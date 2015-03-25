"""This module contains the SQLAlchemy user class definition."""
from flask_login import UserMixin
from sqlalchemy.ext.associationproxy import association_proxy
from server.models.db import db
from server.models.event import Event


class User(db.Model, UserMixin):

    """SQLAlchemy user class definition."""

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column('username', db.String(50), unique=True)
    password = db.Column('password', db.String(50))
    is_admin = db.Column('is_admin', db.Boolean)

    subscriptions = association_proxy('event_subscription', 'event')

    def __init__(self, username, password, is_admin):
        """Constructor for user."""
        self.username = username
        self.password = password
        self.is_admin = is_admin

    # def _get_events_with_role(self, role: str) -> list:
    #    """Get list of events corresponding to a given role.

    #    :param role: role to filter events against (owner)
    #    :return: list of events filtered against the role
    #    """
    #    return list(filter(lambda x: x.role == role, self.events.col))

    # @property
    # def owned_events(self) -> list:
    #    """Get events owned by user.

    #    :return: list of events owned by user
    #    """
    #    return self._get_events_with_role('owner')

    def ownes_event_with_id(self, instance_id: int) -> bool:
        """Tell whether user owns event with a given id."""
        query = Event.query.filter_by(created_by=self.id, id=instance_id)
        event = query.first()
        if event is None:
            return False
        return True
