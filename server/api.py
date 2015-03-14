from flask_restless import ProcessingException
from flask_login import current_user

from server.forms import RegistrationForm
from server.models import User, Keyword, Category, Event


def event_owned_by_current_user(instance_id):
    """Preprocessor for api event DELETE endpoint which
    ensures event can only be deleted by a user with role 'owner'

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
    def preprocessor(data=None):
        form = form_class.from_json(data)
        if not form.validate():
            raise ProcessingException

    return preprocessor


def remove_props(props):
    def preprocessor(data=None):
        for prop in props:
            del data[prop]

    return preprocessor


def login_required_preprocessor(*args, **kwargs):
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
        'methods': ['GET', 'POST', 'DELETE'],
        'preprocessors': {
            'POST': [login_required_preprocessor],
            'DELETE': [
                login_required_preprocessor,
                event_owned_by_current_user
            ]

        },
        'include_columns': ['id',
                            'name',
                            'description',
                            'source',
                            'type',
                            'users',
                            'keywords',
                            'categories',
                            'favorite_users']
    }
]
