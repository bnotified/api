"""This module contains the SQLAlchemy EventSubscription class definition."""
from server.models.db import db


class EventSubscription(db.Model):

    """SQLAlchemy EventSubscription class definition."""

    __tablename__ = 'event_subscriptions'
    user_id = db.Column(
        'user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
    event_id = db.Column(
        'event_id', db.Integer, db.ForeignKey('events.id'), primary_key=True)

    def __init__(self, event_id=None, user_id=None):
        """Constructor for EventSubscription class."""
        self.event_id = event_id
        self.user_id = user_id
