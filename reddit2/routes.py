import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
from reddit2 import app, db, bcrypt
from reddit2.forms import *
from reddit2.models import User, Post
from reddit2.password import *


@app.route('/')
@app.route('/home')
def index():
    posts = Post.query.order_by(Post.dateCreated.desc()).all()
    return render_template('index.html', posts=posts)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegistrationForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashedPassword)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/')
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('auth/login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


def savePicture(form_picture):
    randomName = secrets.token_hex(8)
    _, fExt = os.path.splitext(form_picture.filename)
    pictureFilename = randomName + fExt
    picturePath = os.path.join(app.root_path, 'static/profilePics', pictureFilename)

    outputSize = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(outputSize)
    i.save(picturePath)
    return pictureFilename

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.avatar.data:
            pictureFile = savePicture(form.avatar.data)
            current_user.profilePicture = pictureFile
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account info has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', form=form)

@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been published!', 'success')
        return redirect('/')
    return render_template('post.html', title='Reddit2 - Create A Post',
                            legend='Create A Post', form=form)

@app.route('/post/<int:postId>')
def viewPost(postId):
    post = Post.query.get_or_404(postId)
    return render_template('viewPost.html', post=post)

@app.route('/post/<int:postId>/edit', methods=['GET', 'POST'])
def editPost(postId):
    post = Post.query.get_or_404(postId)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.content.data
        post.edited = True
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('viewPost', postId=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.body
    return render_template('post.html', title='Reddit2 - Edit Post',
                            legend='Edit Post', form=form)

@app.route('/post/<int:postId>/delete', methods=['POST'])
def deletePost(postId):
    post = Post.query.get_or_404(postId)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post was deleted :/')
    return redirect('/')
