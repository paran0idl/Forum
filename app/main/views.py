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
<<<<<<< HEAD
    return render_template('index.html',u_id=uid,user_name=uname,user=user,category=category,posts=posts)

@main.route('/post/<toppost_id>',methods=['get','post'])
def post(toppost_id):
    category = Category.query.all()
    posts=[]
    print toppost_id
    posts.append(Post.query.filter_by(post_id=toppost_id).first())
    for p in Post.query.filter_by(toppost_id=toppost_id).all():
        posts.append(p)
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
    '''
        page = request.args.get('page',1)
        page = int(page)
        hot_post = Essay.query.filter_by(type=etype).filter_by(visible=True).order_by(Essay.visnum.desc()).limit(5).all()
        pagination = Essay.query.filter_by(type=etype).filter_by(visible=True).order_by(Essay.time.desc()).paginate(page,
                        per_page=app.config['PER_PAGE_NUM'],error_out=False)
        eassy = pagination.items
        form = WriteForm()
        # 发帖
        if form.validate_on_submit():
            title = form.name.data #标题
            body = form.text.data #内容
            id = session.get('uid')
=======
    return render_template('index.html',u_id=uid,user_name=uname,user=user)
>>>>>>> 0841001ff1dae91c8c20007870a9f5127c6e9e03

@main.route('/user_center',methods=['get','post'])
@login_required
def user_center():
    name=current_user.user_name
    followed = Follow.query.filter(Follow.follower_id == current_user.u_id).all()
    if followed is not None:
        followed_cnt = len(followed)
    else:
        followed_cnt=0
    fan=Follow.query.filter(Follow.followed_id==current_user.u_id).all()
    if fan is not None:
        fan_cnt = len(fan)
    else:
        fan_cnt = 0
    posts = Post.query.filter(Post.publisher_id==current_user.u_id).all()
    return render_template('user_center.html',name=name,followed=followed,followed_cnt=followed_cnt,fan=fan_cnt,posts=posts)

@main.route('/focus',methods=['get','post'])
@login_required
def focus():
    followed = Follow.query.filter(Follow.follower_id==current_user.u_id).all()
    posts = []
    for i in followed:
        post = Post.query.filter(Post.publisher_id==i.followed_id).all()
        for j in post:
            posts.append(j)
    return render_template('focus.html',posts=posts)

@main.route('/detail',methods=['get','post'])
def detail():
    post_id=request.args.get('post_id')
    toppost=Post.query.filter(Post.post_id==post_id).first()
    comments=Post.query.filter(Post.toppost_id==post_id).all()
    return render_template('detail.html',toppost=toppost,comments=comments)

@main.route('/writepost',methods=['get','post'])
@login_required
def writepost():
    writeform=WriteForm()
<<<<<<< HEAD
    print writeform.name.data
=======
>>>>>>> 0841001ff1dae91c8c20007870a9f5127c6e9e03
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

@main.route('/reply',methods=['get','post'])
@login_required
def reply(toppost_id):
    form=CommentForm()
    if form.validate_on_submit():
        post = Post('reply',
                    form.text.data,
                    current_user.u_id,
                    datetime.now(),
                    toppost_id,
                    1,
                    current_user.user_name
                    )
        db.session.add(post)
        db.session.commit()
    return render_template('reply.html',form=form)
