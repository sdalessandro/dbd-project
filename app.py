# app.py

from flask import Flask, render_template, redirect, url_for, flash, session, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Goal, Task, TimeSlot
from forms import RegistrationForm, LoginForm, GoalForm, TaskForm, TimeSlotForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect, generate_csrf
from markupsafe import escape
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///goals.db'
app.config['SECRET_KEY'] = 'hiu23oghf97023fh3u2f01f13iop1e'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
# Initialize Migrate after setting up app and db
migrate = Migrate(app, db)
# Initialize CSRFProtect
csrf = CSRFProtect(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.debug= True
    app.run()

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    phone_number = request.form.get('phone_number')
    if form.validate_on_submit() and len(phone_number) == 10:
        # Generate a password hash using set_password method
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone_number=phone_number,  # Use the validated phone_number
            password_hash=hashed_password  # Store the hashed password
        )
        db.session.add(new_user)
        try:
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
        except IntegrityError as e:
            db.session.rollback()
            flash('Email is already registered. Please use a different email.', 'danger')
    else:
        print(form.errors)
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
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
            description = form.description.data
            goal_type = form.type.data
            effort_points_raw = form.effort_points.data
            
            # Check if effort_points is provided and is a number
            effort_points = int(effort_points_raw) if effort_points_raw and effort_points_raw.isdigit() else None

            new_goal = Goal(
                description=description,
                type=goal_type,
                effort_points=effort_points,
                user_id=user_id
            )
            db.session.add(new_goal)
            db.session.commit()
            flash('Goal added successfully!', 'success')
        else:
            flash('User not logged in.', 'danger')

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
                description=escape(form.description.data),
                priority=escape(form.priority.data),
                is_completed=form.is_completed.data,
                completed_at=escape(form.completed_at.data),
                user_id=user_id
            )
            db.session.add(new_task)
            db.session.commit()
            print('Task added successfully!', 'success')
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

    return render_template('dashboard.html', csrf_token=generate_csrf(), user=user, goals=goals, tasks=tasks, timeslots=timeslots, goal_form=goal_form, task_form=task_form, timeslot_form=timeslot_form)

@app.route('/user/<int:user_id>/schedule')
def user_schedule(user_id):
    user = User.query.get(user_id)
    goals = Goal.query.filter_by(user_id=user.id).all()
    tasks = Task.query.filter_by(user_id=user.id).all()
    timeslots = TimeSlot.query.filter_by(user_id=user.id).all()
    return render_template('shared_schedule.html', user=user, goals=goals, tasks=tasks, timeslots=timeslots)

@app.route('/complete_tasks', methods=['POST'])
def complete_tasks():
    data = request.json
    task_ids = data.get('task_ids')
    if not task_ids:
        return jsonify({'error': 'No task IDs provided'}), 400
    
    tasks_to_complete = Task.query.filter(Task.id.in_(task_ids))
    for task in tasks_to_complete:
        task.is_completed = True
    db.session.commit()
    
    return jsonify({'success': 'Tasks have been marked as completed.'})

@app.route('/task/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm(obj=task)

    if form.validate_on_submit():
        task.description = form.description.data
        task.priority = form.priority.data
        task.is_completed = form.is_completed.data
        task.completed_at = form.completed_at.data

        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('task_form.html', form=form, task_id=task_id)

@app.route('/delete_tasks', methods=['POST'])
def delete_tasks():
    data = request.json
    task_ids = data.get('task_ids')
    if not task_ids:
        return jsonify({'error': 'No task IDs provided'}), 400
    
    tasks_to_delete = Task.query.filter(Task.id.in_(task_ids))
    for task in tasks_to_delete:
        db.session.delete(task)
    db.session.commit()
    
    return jsonify({'success': 'Tasks have been deleted.'})

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404