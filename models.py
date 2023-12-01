# models.py

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True, nullable=False)

    goals = db.relationship('Goal', backref='user', lazy=True)
    tasks = db.relationship('Task', backref='user', lazy=True)
    timeslots = db.relationship('TimeSlot', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Goal(db.Model):
    __tablename__ = 'goals'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(10), nullable=False)
    effort_points = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    tasks = db.relationship('Task', backref='goal', lazy=True)

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(10))
    is_completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.String)  # Change to String
    
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    timeslots = db.relationship('TimeSlot', backref='task', lazy=True)


class TimeSlot(db.Model):
    __tablename__ = 'timeslots'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(50))
    start_time = db.Column(db.String, nullable=False)
    end_time = db.Column(db.String, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
