#"""This module contains the reported event class."""
#from flask.ext.sqlalchemy import UniqueConstraint
#from server.models.db import db


#class ReportedEvent(db.Model):

#    """ReportedEvent SQLAlchemy table definition."""

#    __tablename__ = 'reported_events'
#    user_id = db.Column(
#        'user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
#    event_id = db.Column(
#        'event_id', db.Integer, db.ForeignKey('events.id'), primary_key=True)

#    event = db.relationship('Event', backref=db.backref('event_user'))
#    user = db.relationship('User', backref=db.backref('event_user'))

#    UniqueConstraint('user_id', 'event_id')

#    def __init__(self, event=None, user=None):
#        """ReportedEvent constructor."""
#        self.event = event
#        self.user = user
