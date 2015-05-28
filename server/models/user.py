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
    uuid = db.Column('uuid', db.Text)

    subscriptions = association_proxy('event_subscriptions', 'event')

    def __init__(self, username, password, is_admin, uuid=None):
        """Constructor for user."""
        self.username = username
        self.password = password
        self.is_admin = is_admin
        self.uuid = uuid

    def owns_event_with_id(self, instance_id: int) -> bool:
        """Tell whether user owns event with a given id."""
        query = Event.query.filter_by(created_by=self.id, id=instance_id)
        event = query.first()
        if event is None:
            return False
        return True

    def is_subscribed_to_event(self, event_id: int) -> bool:
        """Tell whether user is subscribed to event with a given id."""
        filtered = list(filter(
            lambda x: x.id == event_id, self.subscriptions
        ))
        return (len(filtered) > 0)
