from flask_login import UserMixin
from sqlalchemy.ext.associationproxy import association_proxy
from server.models.db import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column('username', db.String(50), unique=True)
    password = db.Column('password', db.String(50))

    events = association_proxy('event_user', 'event')
    favorites = association_proxy('event_favorite', 'event')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def _get_events_with_role(self, role: str) -> list:
        """Gets list of events corresponding to a given role

        :param role: role to filter events against (owner | contributer | designer)
        :return: list of events filtered against the role
        """
        return list(filter(lambda x: x.role == role, self.events.col))

    @property
    def owned_events(self) -> list:
        """Gets events owned by user
        :return: list of events owned by user
        """
        return self._get_events_with_role('owner')

    @property
    def designer_events(self) -> list:
        """Returns list of events user is designer on
        :return: list of designer events
        """
        return self._get_events_with_role('designer')

    @property
    def contributer_events(self) -> list:
        """Returns list of events user is contributer on
        :return: list of contributer events
        """
        return self._get_events_with_role('contributer')

