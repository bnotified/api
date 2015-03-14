from server.models.db import db


class EventUser(db.Model):
    __tablename__ = 'event_users'
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
    event_id = db.Column('event_id', db.Integer, db.ForeignKey('events.id'), primary_key=True)
    role = db.Column('role', db.Enum('owner', 'contributer', 'designer'))

    event = db.relationship('Event', backref=db.backref('event_user'))

    user = db.relationship('User', backref=db.backref('event_user'))

    def __init__(self, event=None, user=None, role=None):
        self.event = event
        self.user = user
        self.role = role