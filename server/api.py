"""This module contains api preprocessors and the api configuration."""
from flask_restless import ProcessingException
from flask_login import current_user

from server.forms import RegistrationForm
from server.models import User, Keyword, Category, Event
from server.logger import logger, logging


def log_post(data):
    """Log data of a POST."""
    logger.log(logging.INFO, data)


def created_by(data):
    """Add current user username to POST data."""
    data['created_by'] = [current_user.username]


def make_non_admin(data):
    """Ensure all users created through registration are non admin."""
    data['is_admin'] = False


def only_admin_can_approve(instance_id: int, data, **kwargs):
    """Ensure only admin users can approve events."""
    if 'is_approved' in data and current_user.is_admin is False:
        raise ProcessingException('Only admins can approve events')


def owner_or_admin_required(instance_id: int, data, **kwargs):
    """Ensure only an event owner or an admin can update an event."""
    if (
        not current_user.owns_event_with_id(instance_id) and
        not current_user.is_admin
    ):
        raise ProcessingException(
            'Only event owners or admins can update this event')


def approved_preprocessor(data):
    """Ensure that events are entered as not approved."""
    data['is_approved'] = current_user.is_admin


def event_owned_by_current_user(instance_id: int):
    """Preprocessor for api event DELETE endpoint.

    Ensures event can only be deleted by a user with role 'owner'

    :param instance_id: id of instance to be deleted
    :raises ProcessingException: if current_user is not an owner of the event
    :return:None
    :rtype: None
    """
    event = Event.query.filter_by(id=instance_id).first()
    owners = event.get_owners()
    if current_user not in owners:
        raise ProcessingException('Only event owners can delete events')


def validate_with_form(form_class):
    """Wrapper for form validating preprocessor."""
    def preprocessor(data=None):
        form = form_class.from_json(data)
        if not form.validate():
            raise ProcessingException

    return preprocessor


def remove_props(props):
    """Wrapper for preprocessor which removes specified props."""
    def preprocessor(data=None):
        for prop in props:
            del data[prop]

    return preprocessor


def login_required_preprocessor(*args, **kwargs):
    """Ensure user is logged in via preprocessor."""
    if not current_user.is_authenticated():
        raise ProcessingException(
            description='Not Authorized',
            code=401
        )
    return True


api_config = [
    {
        'model': User,
        'methods': ['GET', 'POST', 'DELETE'],
        'preprocessors': {
            'POST': [
                make_non_admin,
                validate_with_form(RegistrationForm),
                remove_props(['confirm'])
            ],
        }
    },
    {
        'model': Keyword,
        'methods': ['GET', 'POST', 'DELETE'],
        'preprocessors': {
            'POST': [login_required_preprocessor],
            'DELETE': [login_required_preprocessor]
        }
    },
    {
        'model': Category,
        'methods': ['GET', 'POST', 'DELETE'],
        'preprocessors': {
            'POST': [login_required_preprocessor],

        }
    },
    {
        'model': Event,
        'methods': ['GET', 'POST', 'DELETE', 'PATCH'],
        'preprocessors': {
            'PATCH_SINGLE': [
                owner_or_admin_required,
                only_admin_can_approve
            ],
            'POST': [
                login_required_preprocessor,
                created_by,
                approved_preprocessor
            ],
            'DELETE': [
                login_required_preprocessor,
                event_owned_by_current_user
            ]

        },
        'include_columns': ['id',
                            'name',
                            'description',
                            'subtitle',
                            'start',
                            'end',
                            'created_by',
                            'keywords',
                            'categories',
                            'subscribed_users',
                            'address',
                            'address_name']
    }
]
