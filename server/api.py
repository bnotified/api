"""This module contains api preprocessors and the api configuration."""
from flask_restless import ProcessingException
from flask_login import current_user

from server.forms import RegistrationForm
from server.models import User, Category, Event, EventSubscription
from server.logger import log


def add_current_user(data):
    """Preprocessor that adds the current user as user_id."""
    data["user_id"] = current_user.id


def add_current_user_to_search(search_params=None, **kwargs):
    """Preprocessor that adds the current user as user_id."""
    search_params["filters"][0]["and"].append({
        "name": "user_id",
        "op": "eq",
        "val": current_user.id
    })


def _add_is_current_user_subscribed(event):
    """Add is_subscribed field to a single event dictionary."""
    if current_user is None:
        return
    eid = event["id"]
    event["is_subscribed"] = current_user.is_subscribed_to_event(eid)


def add_is_current_user_subscribed(result=None, **kwargs):
    """Add is_subscribed field to GET event response."""
    if result is None:
        return
    if "objects" in result:
        for event in result["objects"]:
            _add_is_current_user_subscribed(event)
    else:
        _add_is_current_user_subscribed(result)


def _change_subscribed_list_to_count(event):
    """Change the subscribed_users to a count for a singel event dict."""
    event["subscribed_users"] = len(event["subscribed_users"])


def change_subscribed_list_to_count(result=None, **kwargs):
    """Change the subscribed_list to a count."""
    if result is None:
        return
    if "objects" in result:
        for event in result["objects"]:
            _change_subscribed_list_to_count(event)
    else:
        _change_subscribed_list_to_count(result)


def log_post(data):
    """Log data of a POST."""
    log(data)


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


def owner_admin_or_reporting(instance_id: int, data, **kwargs):
    """Ensure an event is either being reported or edited by owner/admin."""
    if (
        not current_user.owns_event_with_id(instance_id) and
        not current_user.is_admin
    ):
        is_reported = data["is_reported"]
        data = {
            "is_reported": is_reported,
        }


def approve_event_only_if_admin(data):
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


def login_required(*args, **kwargs):
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
        'model': Category,
        'methods': ['GET', 'POST', 'DELETE'],
        'preprocessors': {
            'POST': [login_required],

        }
    },
    {
        'model': EventSubscription,
        'methods': ['POST', 'DELETE'],
        'preprocessors': {
            'POST': [
                login_required,
                add_current_user
            ],
            'DELETE_MANY': [
                login_required,
                add_current_user_to_search
            ],
            'DELETE_SINGLE': [
                login_required,
            ],
        },
        'allow_delete_many': True
    },
    {
        'model': Event,
        'methods': ['GET', 'POST', 'PATCH'],
        'preprocessors': {
            'GET_MANY': [
                login_required
            ],
            'GET_SINGLE': [
                login_required
            ],
            'PATCH_SINGLE': [
                owner_admin_or_reporting,
                only_admin_can_approve
            ],
            'POST': [
                login_required,
                created_by,
                approve_event_only_if_admin
            ],
        },
        'postprocessors': {
            'GET_MANY': [
                add_is_current_user_subscribed,
                change_subscribed_list_to_count
            ],
            'GET_SINGLE': [
                add_is_current_user_subscribed,
                change_subscribed_list_to_count
            ],
        },
        'include_columns': ['id',
                            'name',
                            'description',
                            'start',
                            'end',
                            'created_by',
                            'categories',
                            'subscribed_users',
                            'address',
                            'address_name',
                            'is_reported',
                            'is_approved']
    }
]
