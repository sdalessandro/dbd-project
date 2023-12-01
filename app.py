# app.py

from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Goal, Task, TimeSlot
from forms import RegistrationForm, LoginForm, GoalForm, TaskForm, TimeSlotForm
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///goals.db'
app.config['SECRET_KEY'] = 'hiu23oghf97023fh3u2f01f13iop1e'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
# Initialize Migrate after setting up app and db
migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.debug= True
    app.run()


@app.route('/register', methods=['GET', 'POST'])
def register():
    print("hii")
    form = RegistrationForm()
    if form.validate_on_submit():
        print("helloo")
        hashed_password = form.password.data
        new_user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data,
                        email=form.email.data, phone_number=form.phone_number.data, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    else:
        print(form.errors)
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password_hash==form.password.data:
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            print("success")
            return redirect(url_for('dashboard'))
        else:
            print("invalid")
            print(form.errors)
        flash('Invalid credentials.', 'danger')
    return render_template('login.html', form=form)

@app.route('/goal/new', methods=['POST'])
def new_goal():
    form = GoalForm()
    if form.validate_on_submit():
        user_id = session.get('user_id')
        if user_id:
            new_goal = Goal(
                description=form.description.data,
                type=form.type.data,
                effort_points=form.effort_points.data,
                user_id=user_id
            )
            db.session.add(new_goal)
            db.session.commit()
            print('Goal added successfully!', 'success')
        else:
            print('User not logged in.', 'danger')

    # Redirect back to the dashboard, whether or not the form was submitted successfully
    return redirect(url_for('dashboard'))


@app.route('/task/new', methods=['POST'])
def new_task():
    form = TaskForm(request.form)
    print(form.completed_at.data)
    
    if form.validate_on_submit():
        user_id = session.get('user_id')
        if user_id:
            new_task = Task(
                description=form.description.data,
                priority=form.priority.data,
                is_completed=form.is_completed.data,
                completed_at=form.completed_at.data,
                user_id=user_id
            )
            db.session.add(new_task)
            db.session.commit()
            print('Task added successfully!', 'success')
            #print(new_task.completed_at.data,new_task.description)
    else:
        print(form.errors)
        flash('User not logged in.', 'danger')

    # Redirect back to the dashboard, whether or not the form was submitted successfully
    return redirect(url_for('dashboard'))

@app.route('/timeslot/new', methods=['POST'])
def new_timeslot():
    form = TimeSlotForm()
    if form.validate_on_submit():
        user_id = session.get('user_id')
        if user_id:
            new_timeslot = TimeSlot(
                label=form.label.data,
                start_time=form.start_time.data,
                end_time=form.end_time.data,
                user_id=user_id
            )
            db.session.add(new_timeslot)
            db.session.commit()
            print('Timeslot added successfully!', 'success')
    else:
        print(form.errors)
        flash('User not logged in.', 'danger')

    # Redirect back to the dashboard, whether or not the form was submitted successfully
    return redirect(url_for('dashboard'))

# Update the dashboard route to handle form submissions

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    user = User.query.get(session['user_id'])
    goals = Goal.query.filter_by(user_id=user.id).all()
    tasks = Task.query.filter_by(user_id=user.id).all()
    timeslots = TimeSlot.query.filter_by(user_id=user.id).all()

    # Process goal form submission
    goal_form = GoalForm()
    if goal_form.validate_on_submit():
        new_goal = Goal(description=goal_form.description.data, type=goal_form.type.data, effort_points=goal_form.effort_points.data, user_id=user.id)
        db.session.add(new_goal)
        db.session.commit()

    # Process task form submission
    task_form = TaskForm()
    if task_form.validate_on_submit():
        new_task = Task(description=task_form.description.data, priority=task_form.priority.data, is_completed=task_form.is_completed.data, completed_at=task_form.completed_at.data, user_id=user.id)
        
        db.session.add(new_task)
        db.session.commit()

    # Process timeslot form submission
    timeslot_form = TimeSlotForm()
    if timeslot_form.validate_on_submit():
        new_timeslot = TimeSlot(label=timeslot_form.label.data, start_time=timeslot_form.start_time.data, end_time=timeslot_form.end_time.data, user_id=user.id)
        db.session.add(new_timeslot)
        db.session.commit()

    return render_template('dashboard.html', user=user, goals=goals, tasks=tasks, timeslots=timeslots, goal_form=goal_form, task_form=task_form, timeslot_form=timeslot_form)


@app.route('/user/<int:user_id>/schedule')
def user_schedule(user_id):
    user = User.query.get(user_id)
    goals = Goal.query.filter_by(user_id=user.id).all()
    tasks = Task.query.filter_by(user_id=user.id).all()
    timeslots = TimeSlot.query.filter_by(user_id=user.id).all()
    return render_template('shared_schedule.html', user=user, goals=goals, tasks=tasks, timeslots=timeslots)

@app.route('/complete_task/<int:task_id>', methods=['PUT'])
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    is_completed = request.json.get('isCompleted', False)
    task.is_completed = is_completed
    db.session.commit()

    return jsonify({'message': 'Task completion status updated successfully'})

    
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404
