# -*- coding: utf-8 -*-
from flask import redirect,url_for,request
from flask import render_template
from app import login_manager
from flask_login import logout_user,current_user,login_required
from . import main
from app.models import User,Post,Follow
from .forms import  RegisterForm

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route('/register',methods=['get','post'])
def register():
    form = RegisterForm()
    return render_template('register.html', form=form)

@main.route('/logout',methods=['get','post'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/',methods = ['get','post'])
def index():
    uid=''
    uname=''
    if not current_user.is_anonymous:
        uid = current_user.u_id
        uname = current_user.user_name
    return render_template('index.html',u_id=uid,user_name=uname)


@main.route('/user_center')
@login_required
def user_center():
    name=request.args.get('section')
    return render_template('user_center.html',name=name)


@main.route('/focus')
@login_required
def focus():
    posts = []
    followings = Follow.query.filter_by(Follow.follower_id==current_user.u_id).first().following_id
    for i in followings:
        post = Post.query.filter_by(Post.publisher_id==i).first()
        posts.append(post)
    return render_template('focus.html',posts=posts)

@main.route('/detail')
@login_required
def detail(post):
    comments = Post.query.filter_by(Post.toppost_id==post.post_id).first()
    return render_template('detail.html', comments=comments,post=post)