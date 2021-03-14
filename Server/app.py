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
from datetime import datetime

from darkflow.net.build import TFNet
import cv2
import shutil

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
def homepage():
    reports = Report.query.all()

    return render_template("home.html", reports=reports)


@app.route('/_register', methods=['POST'])
def register_mobile():
    if 'login_id' in current_user.__dict__:
        return jsonify("Already logged")

    email = request.form['email']
    password = generate_password_hash(request.form['password'])

    user = User(email=email, password=password)

    db_session.add(user)
    db_session.commit()

    return jsonify("Registered successfully")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'login_id' in current_user.__dict__:
        return redirect(url_for('homepage'))

    if request.method == 'GET':
        return render_template("register.html")
    else:
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        user = User(username=username, password=password)
        db_session.add(user)
        db_session.commit()

        return redirect(url_for('login'))


@app.route('/_login', methods=['POST'])
def login_mobile():
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'login_id' in current_user.__dict__:
        return redirect(url_for('homepage'))

    response = None
    if request.method == 'GET':
        response = make_response(render_template('login.html'))
    else:
        response = make_response(redirect(url_for('homepage')))

        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password,
                                        request.form['password']):
            user.login_id = str(uuid.uuid4())
            db_session.commit()
            login_user(user)
    return response


@app.route('/report', methods=['POST'])
def report():
    # description = request.form['description']
    # location = request.form['location']
    if 'imageFile' in request.files and request.files['imageFile']:
        file = request.files['imageFile']
        filename = file.filename
        filename = filename + "_" + str(datetime.now()) + '.jpeg'
        filename = secure_filename(filename)
        if validate_file_type(filename, ["jpeg", "jpg", "png"]):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            source = f'uploads/{filename}'

            trash_items = get_trash(filename)
            if trash_items == []:
                confirm_trash = "non_trash"
                img_path = f'nontrash/{filename}'
            else:
                confirm_trash = "trash"
                img_path = f'trash/{filename}'
            shutil.move(source, img_path)

            report = Report(
                photo=img_path,
                user_id=1,
                description=" ",
                location=" ",
                confirm_trash=confirm_trash
            )
            db_session.add(report)

        else:
            return jsonify("Invalid photo format")

    else:
        return jsonify("No photo")

    db_session.commit()

    return jsonify(msg="Success")


@app.route('/_logout')
@login_required
def logout_mobile():
    current_user.login_id = None
    db_session.commit()
    logout_user()

    return jsonify("Success")


@app.route('/logout')
@login_required
def logout():
    current_user.login_id = None
    db_session.commit()
    logout_user()

    return redirect(url_for("homepage"))


@app.route('/add_report', methods=['GET', 'POST'])
@login_required
def add_report():
    if request.method == 'GET':
        return render_template("add_report.html")
    else:
        location = request.form['location']
        description = request.form['description']

    if 'imageFile' in request.files and request.files['imageFile']:
        file = request.files['imageFile']
        filename = file.filename
        filename = secure_filename(filename)
        if validate_file_type(filename, ["jpeg", "jpg", "png"]):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            source = f'uploads/{filename}'

            trash_items = get_trash(filename)
            if trash_items == []:
                confirm_trash = "non_trash"
                img_path = f'nontrash/{filename}'
            else:
                confirm_trash = "trash"
                img_path = f'trash/{filename}'
            shutil.move(source, img_path)
            report = Report(
                photo=source,
                user_id=current_user.id,
                description=description,
                location=location,
                confirm_trash="trash"
            )
            db_session.add(report)

    db_session.commit()


    return redirect(url_for('homepage'))


def get_trash(filename):
    options = {"metaLoad": "built_graph/tiny-yolo-voc-13c.meta",
               "pbLoad": "built_graph/tiny-yolo-voc-13c.pb", "threshold": 0.3}
    tfnet = TFNet(options)
    path = f'uploads/{filename}'
    imgcv = cv2.imread(path)
    trash = tfnet.return_predict(imgcv)
    return trash
