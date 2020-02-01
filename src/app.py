import json
from db import db, Habit, Event
from flask import Flask, request

app = Flask(__name__)
db_filename = 'habits.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
