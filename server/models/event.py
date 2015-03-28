"""This module contains the Event class."""
from sqlalchemy.ext.associationproxy import association_proxy

from server.models.db import db


class Event(db.Model):

    """SQLAlchemy model definition for the event class."""

    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    is_approved = db.Column(db.Boolean)
    is_reported = db.Column(db.Boolean)
    created_by = db.Column(db.String(50))
    address = db.Column(db.Text)
    address_name = db.Column(db.Text)

    # users = association_proxy('event_user', 'user')
    subscribed_users = association_proxy('event_subscriptions', 'user')
    categories = db.relationship('Category', secondary='event_categories')
    keywords = db.relationship('Keyword', secondary='event_keywords')

    # def _get_users_with_role(self, role: str) -> list:
    #    """Return a list of users corresponding to the event with a role.

    #    :param role: role of user | owner || contributer || designer
    #    :return: list of users corresponding to the given role
    #    """
    #    return list(filter(lambda x: x.role == role, self.users.col))

    # @property
    # def owners(self) -> list:
    #    """Return a list of event owners.

    #    :return: a list of usernames of event owners
    #    """
    #    return self._get_users_with_role('owner')

    # @property
    # def contributers(self) -> list:
    #    """Return a list of event contributers.

    #    :return: a list of event contributers
    #    """
    #    return self._get_users_with_role('contributer')
