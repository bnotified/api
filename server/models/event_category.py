from server.models.db import db


class EventCategory(db.Model):
    __tablename__ = 'event_categories'
    category_id = db.Column(
        'category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
    event_id = db.Column(
        'event_id', db.Integer, db.ForeignKey('events.id'), primary_key=True)
