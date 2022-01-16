from flask import Flask, render_template, request, Response, session, flash, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import json
import os
import smtplib
import email
import pymysql
import requests
import math
pymysql.install_as_MySQLdb()

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


email_address = 'demo.newark@gmail.com'
email_password = 'newark123###'

message = email.message.EmailMessage()
message["From"] = email_address

with open('config.json', 'r') as C:
    params = json.load(C)['params']

local_server = params['local_server']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = params['upload_location']
app.secret_key = '1aa518aa67cc306ff11c92d45b7a3bd3'
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    # MAIL_USE_TLS=True,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=os.environ.get('GMAIL_USERNAME'),
    MAIL_PASSWORD=os.environ.get('GMAIL_PASSWORD'),
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
db = SQLAlchemy(app)


class Contacts(db.Model):
    s_no = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(25), unique=False, nullable=False)
    email_user = db.Column(db.String(50), unique=False, nullable=False)
    phone_num = db.Column(db.Integer(), unique=False, nullable=False)
    mssg = db.Column(db.String(150), unique=False, nullable=False)
    date = db.Column(db.String(12), unique=False, nullable=True)

    # def __repr__(self):
    #     return '<User %r>' % self.name


class Posts(db.Model):
    sno = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(50), unique=False, nullable=False)
    slug = db.Column(db.String(35), unique=False, nullable=False)
    content = db.Column(db.String(100), unique=False, nullable=False)
    date = db.Column(db.String(12), unique=False, nullable=True)
    img_file = db.Column(db.String(12), unique=False, nullable=True)
    tagline = db.Column(db.String(), unique=False, nullable=True)

    # def __repr__(self):
    #     return '<User %r>' % self.name



@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/dashboard')


@app.route("/")
def home():
    flash('Welcome')
    posts = Posts.query.filter_by().all()
    last = math.ceil(len(posts) / int(params['no_of_posts']))
    page = request.args.get('number')
    print(last)
    if not str(page).isnumeric():
        page = 1
    page = int(page)
    posts = posts[(page-1)*int(params['no_of_posts']):page*int(params['no_of_posts'])]
    # Pagination
    # First
    # [0:params['no_of_posts']]
    if page == 1:
        prev = "#"
        next_page = "/?number="+str(page+1)
    elif page == last:
        prev = "/?number="+str(page-1)
        next_page = "#"
    else:
        prev = "/?number="+str(page-1)
        next_page = "/?number="+str(page+1)

    return render_template('index.html', params=params, posts=posts, prev=prev, next_page=next_page)


@app.route('/about')
def about():
    return render_template('about.html', params=params)


@app.route('/delete/<string:sno>', methods=['GET', 'POST'])
def delete(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        post_del = Posts.query.filter_by(sno=sno).first()
        db.session.delete(post_del)
        db.session.commit()
    return redirect('/dashboard')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' in session and session['user'] == params['admin_user']:
        posts = Posts.query.all()
        flash('Welcome back')
        return render_template('dashboard.html', params=params, posts=posts)
    else:
        if request.method == 'POST':
            username = request.form.get('uname')
            userpass = request.form.get('pass')
            if username == params['admin_user'] and userpass == params['admin_password']:
                # Set session variable
                posts = Posts.query.all()
                session['user'] = username
                flash("Welcome, You are logged in.")
                return render_template('dashboard.html', params=params, posts=posts)
            else:
                return render_template('login.html', params=params)
        else:
            return render_template('login.html', params=params)


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        f = request.files['file']

        if f.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))

        f.save(os.path.join(app.config['UPLOAD_FOLDER']))


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        """Add entry to database"""
        name = request.form.get('name')
        email_user = request.form.get('email_user')
        phone_num = request.form.get('phone_num')
        mssg = request.form.get('message')
        entry = Contacts(name=name, email_user=email_user, mssg=mssg, date=datetime.now(), phone_num=phone_num)
        try:
            db.session.add(entry)
            db.session.commit()
            message["Subject"] = "Welcome To Vashesh's Page"
            message.set_content("Hello {}, Your message has been received. We wil soon reply to you\n"
                                "The following details have been received:\nPhone: {}\nEmail: {}\nMessage: "
                                "{}".format(name, phone_num, email_user, mssg))
            source123 = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            source123.login(email_address, email_password)
            message['To'] = email_user
            source123.send_message(message)
            message.__delitem__('To')
            message.__delitem__('Subject')
            source123.quit()
            flash('Message Sent.', "success")
        except Exception as e:
            flash('{} '.format(e), "danger")
    return render_template('contact.html', params=params)


@app.route('/post/<string:post_slug>', methods=['GET'])
def post_route(post_slug):
    posts = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=params, post=posts)


@app.route('/edit/<string:sno>', methods=['GET', 'POST'])
def edit(sno):
    if "user" in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            box_title = request.form.get('title')
            tagline = request.form.get('tagline')
            slug = request.form.get('slug')
            content = request.form.get('content')
            img_file = request.form.get('img_file')
            if sno == '0':
                posting = Posts(title=box_title, slug=slug, content=content, img_file=img_file, date=datetime.now(),
                                tagline=tagline)
                db.session.add(posting)
                db.session.commit()
            else:
                posting = Posts.query.filter_by(sno=sno).first()
                posting.title = box_title
                posting.tagline = tagline
                posting.slug = slug
                posting.content = content
                posting.img_file = img_file
                posting.date = datetime.now()
                db.session.commit()
                return redirect('/edit/'+sno)
    posts = Posts.query.filter_by(sno=sno).first()
    return render_template('edit.html', params=params, posts=posts, sno=sno)


@app.route('/post')
def post():
    return render_template('post.html', params=params)


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
)


if __name__ == "__main__":
    app.run(debug=True)
