from server.models.db import db


class EventFavorite(db.Model):
    __tablename__ = 'event_favorites'
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
    event_id = db.Column('event_id', db.Integer, db.ForeignKey('events.id'), primary_key=True)

    event = db.relationship('Event', backref=db.backref('event_favorite'))

    user = db.relationship('User', backref=db.backref('event_favorite'))

    def __init__(self, event=None, user=None):
        self.event = event
        self.user = user