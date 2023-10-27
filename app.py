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
    app.run(debug=True)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data,
                        email=form.email.data, phone_number=form.phone_number.data, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials.', 'danger')
    return render_template('login.html', form=form)

@app.route('/goal/new', methods=['GET', 'POST'])
def new_goal():
    form = GoalForm()
    if form.validate_on_submit():
        goal = Goal(description=form.description.data, type=form.type.data, effort_points=form.effort_points.data, user_id=session['user_id'])
        db.session.add(goal)
        db.session.commit()
        flash('Goal added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('goal_form.html', form=form)

@app.route('/task/new', methods=['GET', 'POST'])
def new_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(description=form.description.data, priority=form.priority.data, is_completed=form.is_completed.data, completed_at=form.completed_at.data, user_id=session['user_id'])
        db.session.add(task)
        db.session.commit()
        flash('Task added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('task_form.html', form=form)

@app.route('/timeslot/new', methods=['GET', 'POST'])
def new_timeslot():
    form = TimeSlotForm()
    if form.validate_on_submit():
        timeslot = TimeSlot(label=form.label.data, start_time=form.start_time.data, end_time=form.end_time.data, user_id=session['user_id'])
        db.session.add(timeslot)
        db.session.commit()
        flash('Timeslot added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('timeslot_form.html', form=form)

@app.route('/dashboard')
def dashboard():
    user = User.query.get(session['user_id'])
    goals = Goal.query.filter_by(user_id=user.id).all()
    tasks = Task.query.filter_by(user_id=user.id).all()
    timeslots = TimeSlot.query.filter_by(user_id=user.id).all()
    return render_template('dashboard.html', user=user, goals=goals, tasks=tasks, timeslots=timeslots)

@app.route('/user/<int:user_id>/schedule')
def user_schedule(user_id):
    user = User.query.get(user_id)
    goals = Goal.query.filter_by(user_id=user.id).all()
    tasks = Task.query.filter_by(user_id=user.id).all()
    timeslots = TimeSlot.query.filter_by(user_id=user.id).all()
    return render_template('shared_schedule.html', user=user, goals=goals, tasks=tasks, timeslots=timeslots)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404
