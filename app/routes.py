from functools import wraps
from flask import Flask
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from datetime import datetime
from flask import session


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        user = User.query.filter_by(
            username=username, hashed_password=hashed_password).first()

        if user:
            session['user_id'] = user.id
            return redirect(url_for('index.html'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    # Record logout time
    user_session = UserSession.query.filter_by(
        user_id=session['user_id'], logout_time=None).first()
    if user_session:
        user_session.logout_time = func.now()
        db.session.commit()

    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route('/test')
@login_required
def test():
    return 'Welcome to the test page'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        user = User(username=username, hashed_password=hashed_password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/questions')
@login_required
def questions():
    # Retrieve the current question from the QB
    question = get_question_from_QB(session['current_question'])
    return render_template('questions.html', question=question)


@app.route('/results')
@login_required
def results():
    user = User.query.get(session['user_id'])
    return render_template('results.html', score=user.score)


@app.route('/leaderboard')
def leaderboard():
    users = User.query.order_by(User.score.desc()).limit(10).all()
    return render_template('leaderboard.html', users=users)


@app.route('/submit_question/<int:question_id>', methods=['POST'])
def submit_question(question_id):
    question = get_question_by_id(question_id)
    user_answer = request.form['answer']
    is_correct = submit_answer_to_QB(question, user_answer)

    current_question_index = session['current_question']
    session['attempts'][current_question_index] += 1

    if is_correct:
        attempts = session['attempts'][current_question_index]
        if attempts == 1:
            session['score'] += 3
        elif attempts == 2:
            session['score'] += 2
        elif attempts == 3:
            session['score'] += 1

        # Move to the next question
        session['current_question'] += 1
    else:
        if session['attempts'][current_question_index] >= 3:
            correct_output = get_correct_output_from_QB(question)
            incorrect_output = get_incorrect_output_from_QB(
                question, user_answer)
            return render_template('comparison.html', incorrect_output=incorrect_output, correct_output=correct_output)
        else:
            return render_template('incorrect.html', question=question)

    return redirect(url_for('questions'))


# Implement the functions to interact with the Question-Banks (QB)
def get_question_from_QB(question_index):
    # Retrieve the question from the QB using bespoke API.
    return question