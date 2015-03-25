"""This module contains the SQLAlchemy EventSubscription class definition."""
from server.models.db import db


class EventSubscription(db.Model):

    """SQLAlchemy EventSubscription class definition."""

    __tablename__ = 'event_subscriptions'
    user_id = db.Column(
        'user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
    event_id = db.Column(
        'event_id', db.Integer, db.ForeignKey('events.id'), primary_key=True)

    event = db.relationship('Event', backref=db.backref('event_subscriptions'))

    user = db.relationship('User', backref=db.backref('event_subscriptions'))

    def __init__(self, event=None, user=None):
        """Constructor for EventSubscription class."""
        self.event = event
        self.user = user
