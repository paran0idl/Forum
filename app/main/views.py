# -*- coding: utf-8 -*-
from flask import redirect,url_for,request
from flask import render_template
from app import login_manager
from flask_login import logout_user,current_user,login_required
from . import main
from app.models import User,Post,Follow
from .forms import RegisterForm,WriteForm,CommentForm
from datetime import datetime
from .. import db
from ..models import Category

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route('/register',methods=['get','post'])
def register():
    form = RegisterForm()
    return render_template('register.html', form=form)

@main.route('/login',methods=['get','post'])
def login():
    return render_template('login.html')

@main.route('/logout',methods=['get','post'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/admin',methods=['get','post'])
def admin():
    return redirect('/admin')

@main.route('/',methods = ['get','post'])
def index():

    category=Category.query.all()
    uid=''
    uname=''
    posts=Post.query.filter_by(toppost_id=0).all()
    if not current_user.is_anonymous:
        uid = current_user.u_id
        uname = current_user.user_name
        user=current_user
    else:
        user=None

    return render_template('index.html',u_id=uid,user_name=uname,user=user,category=category,posts=posts)


@main.route('/post/<toppost_id>',methods=['get','post'])
def post(toppost_id):
    category = Category.query.all()
    posts=[]
    print toppost_id
    posts.append(Post.query.filter_by(post_id=toppost_id).first())
    for p in Post.query.filter_by(toppost_id=toppost_id).all():
        posts.append(p)
    posts = Post.query.order_by(Post.post_time.asc()).all()
    uid = ''
    uname = ''
    if not current_user.is_anonymous:
        uid = current_user.u_id
        uname = current_user.user_name
        user = current_user
    else:
        user = None
    return render_template('Posts.html',u_id=uid,user_name=uname,user=user,category=category,posts=posts)

@main.route('/category/<category_id>',methods=['get','post'])
def category(category_id):
    posts=[]
    posts=Post.query.filter_by(category_id=category_id).all()
    uid = ''
    uname = ''
    if not current_user.is_anonymous:
        uid = current_user.u_id
        uname = current_user.user_name
        user = current_user
    else:
        user = None
    return render_template('index.html', u_id=uid, user_name=uname, user=user, category=category, posts=posts)

@main.route('/writepost',methods=['get','post'])
@login_required
def writepost():
    writeform=WriteForm()
    if writeform.validate_on_submit():
        post = Post(writeform.name.data,
                    writeform.text.data,
                    current_user.u_id,
                    datetime.now(),
                    0,
                    1,
                    current_user.user_name
                    )
        db.session.add(post)
        db.session.commit()
    return render_template('WritePost.html',form=writeform)