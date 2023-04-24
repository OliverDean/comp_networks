from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    hashed_password = db.Column(db.String(128), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())

    sessions = relationship('UserSession', back_populates='user')
    question_attempts = relationship('UserQuestionAttempt', back_populates='user')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    login_time = db.Column(db.DateTime, default=func.now())
    logout_time = db.Column(db.DateTime, nullable=True)
    duration = db.Column(db.Integer, nullable=True)

    user = relationship('User', back_populates='sessions')


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(255), nullable=False)
    question_type = db.Column(db.Enum('multi_choice', 'programming_challenge'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())

    question_attempts = relationship('UserQuestionAttempt', back_populates='question')


class UserQuestionAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    attempt_number = db.Column(db.Integer, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    submitted_answer = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())

    user = relationship('User', back_populates='question_attempts')
    question = relationship('Question', back_populates='question_attempts')

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
