from server.models.db import db


class EventCategory(db.Model):
    __tablename__ = 'event_categories'
    category_id = db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
    event_id = db.Column('event_id', db.Integer, db.ForeignKey('events.id'), primary_key=True)

    event = db.relationship('Event', backref=db.backref('event_category'))

    category = db.relationship('Category', backref=db.backref('event_category'))

    def __init__(self, event=None, category=None):
        self.event = event
        self.category = category