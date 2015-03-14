from server.models.db import db


class EventKeyword(db.Model):
    __tablename__ = 'event_keywords'
    keyword_id = db.Column('keyword_id', db.Integer, db.ForeignKey('keywords.id'), primary_key=True)
    event_id = db.Column('event_id', db.Integer, db.ForeignKey('events.id'), primary_key=True)

    event = db.relationship('Event', backref=db.backref('event_keyword'))

    keyword = db.relationship('Keyword', backref=db.backref('event_keyword'))

    def __init__(self, event=None, keyword=None, role=None):
        self.event = event
        self.keyword = keyword
        self.role = role