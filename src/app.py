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
        assert 'user_id' in post_body
        assert 'name' in post_body
    except:
        res = {'success': False, 'error': 'User_id or name was not provided.'}
        return json.dumps(res), 400
    
    user_id = post_body.get('user_id')
    name = post_body.get('name')
    notes = post_body.get('notes', '')
    habit = Habit(
        user_id = user_id,
        name = name,
        notes = notes
    )
    db.session.add(habit)
    db.session.commit()
    return json.dumps({'success': True, 'data': habit.serialize()}), 201

@app.route('/api/habits/<int:habit_id>/')
def get_habit(habit_id):
    habit = Habit.query.filter_by(id=habit_id).first()
    if not habit:
        return json.dumps({'success': False, 'error': 'Habit not found'}), 404
    return json.dumps({'success': True, 'data': habit.serialize()}), 200

@app.route('/api/habits/<int:habit_id>/', methods=['POST'])
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

# Your routes here
'''
@app.route('/api/courses/')
def get_all_courses():
    courses = Course.query.all()
    res = {'success': True, 'data': [c.serialize() for c in courses]}
    return json.dumps(res), 200

@app.route('/api/courses/', methods=['POST'])
def create_course():
    post_body = json.loads(request.data)
    code = post_body.get('code', '')
    name = post_body.get('name', '')
    course = Course(
        code=code,
        name=name
    )
    db.session.add(course)
    db.session.commit()
    return json.dumps({'success': True, 'data': course.serialize()}), 201

@app.route('/api/course/<int:course_id>/')
def get_course(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if not course:
        return json.dumps({'success': False, 'error': 'Course not found!'}), 404
    return json.dumps({'success': True, 'data': course.serialize()}), 200

@app.route('/api/users/', methods=['POST'])
def create_user():
    post_body = json.loads(request.data)
    name = post_body.get('name', '')
    netid = post_body.get('netid', '')
    user = User(
        name=name,
        netid=netid
    )
    db.session.add(user)
    db.session.commit()
    data = user.serialize()
    data['course'] = []
    return json.dumps({'success': True, 'data': data}), 201

@app.route('/api/user/<user_id>/')
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    data = user.serialize()
    data['courses'] = [s.serialize() for s in user.student_course]
    instructors = [i.serialize for i in user.instructor_course]
    for i in instructors:
        data['courses'].append(i)
    return json.dumps({'success': True, 'data': data}), 200

@app.route('/api/course/<int:course_id>/add/', methods=['POST'])
def add_user_to_course(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if not course:
        return json.dumps({'success': False, 'error': 'Course not found!'}), 404
    post_body = json.loads(request.data)
    user_type = post_body.get('type')
    user_id = post_body.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    if user_type == 'instructor':
        course.instructors.append(user)
    elif user_type == 'student':
        course.students.append(user)
    # TODO Correct error code?
    else:
        return json.dumps({'success': False, 'error': 'Invalid user type'}), 401
    db.session.commit()
    return json.dumps({'success': True, 'data': course.serialize()}), 200

@app.route('/api/course/<int:course_id>/assignment/', methods=['POST'])
def create_assignment(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if not course:
        return json.dumps({'success': False, 'error': 'Course not found!'}), 404
    post_body = json.loads(request.data)
    title = post_body.get('title', '')
    due_date = post_body.get('due_date')
    assignment = Assignment(
        title=title,
        due_date=due_date
    )
    course.assignments.append(assignment)
    db.session.add(assignment)
    db.session.commit()
    return json.dumps({'success': True, 'data': assignment.serialize()}), 201
'''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
