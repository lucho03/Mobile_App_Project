import uuid
import os


from flask import Flask
from flask import render_template, request,\
    redirect, make_response, url_for, jsonify

from functools import wraps


from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from database import db_session, init_db
from login import login_manager
from models import User, Company, Report


from utils import validate_file_type
from flask.json import jsonify
import json


app = Flask(__name__)

app.secret_key = "jsfejkawfoeawnfoieawnfpneawipnf"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['UPLOAD_FOLDER'] = './uploads'

login_manager.init_app(app)
init_db()

app.add_url_rule('/uploads/<filename>', 'uploaded_file', build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads':  app.config['UPLOAD_FOLDER']
})


@app.teardown_appcontext
def shutdown_context(exception=None):
    db_session.remove()


@app.route('/')
def home():
    reports = Report.query.all()

    return render_template("index.html", reports=reports)


@app.route('/register', methods=['POST'])
def register():
    if 'login_id' in current_user.__dict__:
        return jsonify("Already logged")

    email = request.form['email']
    password = generate_password_hash(request.form['password'])

    user = User(email=email, password=password)

    db_session.add(user)
    db_session.commit()

    return jsonify("Registered successfully")


@app.route('/login', methods=['POST'])
def login():
    if 'login_id' in current_user.__dict__:
        return jsonify("Already logged")


    username = request.form['username']
    password = request.form['password']

    user = User.query.filter(User.username == username).first()

    if user and check_password_hash(user.password, password):
        user.login_id = str(uuid.uuid4())
        db_session.commit()
        login_user(user)

        return jsonify("Success")
    else:
        return jsonify("Error")


@app.route('/report', methods=['POST'])
@login_required
def report():
    description = request.form['description']
    location = request.form['location']
    
    if 'photo' in request.files and request.files['photo']:
            file = request.files['photo']
            filename = secure_filename(file.filename)

            if validate_file_type(filename, ["jpeg", "jpg", "png"]):
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                report = Report(
                    photo=f'/uploads/{filename}',
                    user_id=current_user.id,
                    description=description,
                    location=location)

                db_session.add(report)
            else:
                return jsonify("Invalid photo format")
    else:
        return jsonify("No photo")

    db_session.commit()

    return jsonify("Success")


@app.route('/logout')
@login_required
def logout():
    current_user.login_id = None
    db_session.commit()
    logout_user()

    return jsonify("Success")

