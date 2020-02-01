from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Habit(db.Model):
    __tablename__ = 'habit'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    events = db.relationship('Event', cascade='delete', back_populates='habit')
    notes = db.Column(db.String, nullable=False)
    done = db.Column(db.Boolean, nullable=False)

    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.name = kwargs.get('name')
        self.events = []
        self.notes = kwargs.get('notes')
        self.done = False

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'notes': self.notes,
            'done': self.done
        }

    def set_name(self, name):
        self.name = name

    def set_notes(self, notes):
        self.notes = notes

    def set_done(self, done):
        self.done = done


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    # whether the event is done, not done, or skip
    category = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
    habit = db.relationship('Habit', back_populates='events')
    skip_note = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        assert 'category' in kwargs
        self.category = kwargs.get('category')
        self.date = kwargs.get('date')
        assert 'habit_id' in kwargs
        self.habit_id = kwargs.get('habit_id')
        self.skip_note = kwargs.get('skip_note')

    def serialize(self):
        return {
            'id': self.id,
            'category': self.category,
            'date': self.date,
            'habit_id': self.habit_id,
            'skip_note': self.skip_note
        }

# class SkipNote(db.Model):
#     __tablename__ = 'skipnote'
#     id = db.Column(db.Integer, primary_key=True)
#     note = db.Column(db.String, nullable=False)
#     event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
#     event = db.relationship('Event', back_populates='skipnotes')
