from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
FORMAT = '%c'

# Your classes here
class Habit(db.Model):
    __tablename__ = 'habit'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    events = db.relationship('Event', cascade='delete', back_populates='habit')
    notes = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.name = kwargs.get('name')
        self.events = []
        self.notes = kwargs.get('notes')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'notes': self.notes
        }
    
    def set_name(self, name):
        self.name = name
        
    def set_notes(self, notes):
        self.notes = notes

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
        self.category = kwargs['category']
        self.date = datetime.now().strftime(FORMAT)
        assert 'habit_id' in kwargs
        self.habit_id = kwargs['habit_id']
        self.skip_note = kwargs.get('skip_note', '')
    
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
    


'''
student_association_table = db.Table('student_association', db.Model.metadata,
    db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

instructor_association_table = db.Table('instructor_association', db.Model.metadata,
    db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    assignments = db.relationship('Assignment', cascade='delete', back_populates='course')
    instructors = db.relationship('User', secondary=instructor_association_table, back_populates='instructor_course')
    students = db.relationship('User', secondary=student_association_table, back_populates='student_course')

    def __init__(self, **kwargs):
        self.code = kwargs.get('code', '')
        self.name = kwargs.get('name', '')
        self.assignments = []
        self.instructors = []
        self.students = []

    def serialize(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'assignments': [a.serialize() for a in self.assignments],
            'instructors': [i.serialize() for i in self.instructors],
            'students': [s.serialize() for s in self.students]
        }

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False)
    instructor_course = db.relationship('Course', secondary=instructor_association_table)
    student_course = db.relationship('Course', secondary=student_association_table)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.netid = kwargs.get('netid', '')
        instructor_course = []
        student_course = []
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'netid': self.netid
        }

class Assignment(db.Model):
    __tablename__ = 'assignment'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    # TODO make sure Integer can actually hold long due dates
    due_date = db.Column(db.Integer, nullable=False)
    # TODO check to make sure the following sets up an actual one-to-many btw Course and Assignment
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    course = db.relationship('Course', back_populates='assignments')

    def __init__(self, **kwargs):
        self.title = kwargs.get('title', '')
        self.due_date = kwargs.get('due_date', 0)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'due_date': self.due_date,
            # TODO figure out how to serialize a course with only some information
            # Also, can I even use the course id to directly get the course?
            'course': {
                'id': self.course.id,
                'code': self.course.code,
                'name': self.course.name
            }
        }
'''
