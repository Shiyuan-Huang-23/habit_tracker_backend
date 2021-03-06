import json
import schedule
import time
from datetime import datetime
from db import db, Habit, Event
from flask import Flask, request

app = Flask(__name__)
db_filename = 'habits.db'
FORMAT = '%x'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()


def reset_habits():
    habits = Habit.query.all()
    for habit in habits:
        habit.set_done(False)


@app.route('/api/habits/')
def get_all_habits():
    habits = Habit.query.all()
    res = {'success': True, 'data': [h.serialize() for h in habits]}
    return json.dumps(res), 200


@app.route('/api/habits/', methods=['POST'])
def create_habit():
    post_body = json.loads(request.data)
    try:
        # assert 'user_id' in post_body
        assert 'name' in post_body
    except:
        res = {'success': False, 'error': 'User_id or name was not provided.'}
        return json.dumps(res), 400

    user_id = post_body.get('user_id', 1)
    name = post_body.get('name')
    notes = post_body.get('notes', '')
    habit = Habit(
        user_id=user_id,
        name=name,
        notes=notes
    )
    db.session.add(habit)
    db.session.commit()
    return json.dumps({'success': True, 'data': habit.serialize()}), 201


@app.route('/api/habit/<int:habit_id>/')
def get_habit(habit_id):
    habit = Habit.query.filter_by(id=habit_id).first()
    if not habit:
        return json.dumps({'success': False, 'error': 'Habit not found'}), 404
    return json.dumps({'success': True, 'data': habit.serialize()}), 200


@app.route('/api/habit/<int:habit_id>/done/', methods=['POST'])
def mark_done(habit_id):
    habit = Habit.query.filter_by(id=habit_id).first()
    if not habit:
        return json.dumps({'success': False, 'error': 'Habit not found'}), 404
    habit.set_done(True)
    event = Event(
        category='done',
        date=datetime.now().strftime(FORMAT),
        habit_id=habit_id,
        skip_note=''
    )
    db.session.add(event)
    db.session.commit()

    return json.dumps({'success': True, 'data': habit.serialize()}), 200


@app.route('/api/habit/<int:habit_id>/', methods=['POST'])
def edit_habit(habit_id):
    habit = Habit.query.filter_by(id=habit_id).first()
    if not habit:
        return json.dumps({'success': False, 'error': 'Habit not found'}), 404

    post_body = json.loads(request.data)
    name = post_body.get('name', habit.name)
    notes = post_body.get('notes', habit.notes)
    habit.set_name(name)
    habit.set_notes(notes)
    db.session.commit()

    return json.dumps({'success': True, 'data': habit.serialize()}), 201


@app.route('/api/habits/<int:habit_id>/', methods=['DELETE'])
def delete_habit(habit_id):
    habit = Habit.query.filter_by(id=habit_id).first()
    if not habit:
        return json.dumps({'success': False, 'error': 'Habit not found'}), 404
    db.session.delete(habit)
    db.session.commit()

    return json.dumps({'success': True, 'data': habit.serialize()}), 200


@app.route('/api/events/<int:habit_id>/')
def get_all_events(habit_id):
    events = Event.query.filter_by(habit_id=habit_id)
    return json.dumps({'success': True, 'data': [e.serialize() for e in events]})


@app.route('/api/event/<int:habit_id>/', methods=['POST'])
def create_event(habit_id):
    habit = Habit.query.filter_by(id=habit_id).first()
    if not habit:
        return json.dumps({'success': False, 'error': 'Invalid habit id'}), 404
    post_body = json.loads(request.data)
    category = post_body.get('category')
    skip_note = post_body.get('skip_note', '')
    today = datetime.now().strftime(FORMAT)
    date = post_body.get('date', today)
    try:
        event = Event(
            category=category,
            date=date,
            habit_id=habit_id,
            skip_note=skip_note
        )
        if category == 'skip' and date == today:
            habit.set_done(True)
        db.session.add(event)
        db.session.commit()
    except:
        return json.dumps({'success': False, 'error': 'Error in creating event'}), 500

    return json.dumps({'success': True, 'data': event.serialize()}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
