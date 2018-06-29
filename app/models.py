# -*- coding: utf-8 -*-
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager
import six  #get_id
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import time
from flask_sqlalchemy import SQLAlchemy
from app import create_app

class Permission:
    FOLLOW = 0X01
    ADMIN = 0X04

class User(UserMixin,db.Model):
    __tablename__='user'
    u_id = db.Column(db.Integer,primary_key=True,index=True,autoincrement=True)
    user_name=db.Column(db.String(64),unique=True)
    user_email=db.Column(db.String(64),unique=True)
    user_pwd=db.Column(db.String(64))
    user_permission=db.Column(db.Integer,default=Permission.FOLLOW)
    avatar=db.Column(db.LargeBinary)
    email_confirm=db.Column(db.Boolean,default=0)
    user_score=db.Column(db.Integer,default=0)

    post=db.relationship('Post',backref='post_author', lazy='dynamic')
    def __repr__(self):
        return '<User: %s>' % (self.username)

    def get_id(self):
        try:
            return six.text_type(self.u_id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

class Admin(User):
    def add_score(self,u_id,num):
        result = User.query.filter_by(User.u_id==u_id).first()
        result.user_score+=num
        db.session.commit()

    def del_user(self,u_id):
        result = User.qury.filter_by(User.u_id==u_id).first()
        db.session.delete(result)
        db.session.commit()

    def del_post(self,p_id):
        result = post.query.filter_by(post.post_id==p_id).first()
        db.session.delete(result)
        db.session.commit()

class Post(db.Model):
    __tablename__='post'
    post_id=db.Column(db.Integer,primary_key=True,index=True,autoincrement=True)
    title=db.Column(db.UnicodeText)
    content=db.Column(db.UnicodeText)
    publisher_id=db.Column(db.Integer,db.ForeignKey('user.u_id'))
    post_time=db.Column(db.DateTime, index=True, default=datetime.utcnow)
    toppost_id=db.Column(db.Integer)
    category_id=db.Column(db.Integer)
    post_score=db.Column(db.Integer,default=0)

    def __init__(self,post_id,title,content,publisher_id,post_time,toppost_id,category_id):
        self.post_id = post_id
        self.title = title
        self.content = content
        self.publisher_id = publisher_id
        self.post_time = post_time,
        self.toppost = toppost_id,
        self.category = category_id

class Category(db.Model):
    __tablename__='category'
    category_id=db.Column(db.Integer,primary_key=True,index=True,autoincrement=True,unique=True)
    topic_id=db.Column(db.Integer)

    def __init__(self,category_id,topic_id):
        self.category_id = category_id
        self.topic_id = topic_id

class Follow(db.Model):
    __tablename__='follow'
    follow_info=db.Column(db.Integer,primary_key=True,index=True,autoincrement=True,unique=True)
    following_id=db.Column(db.Integer)
    follower_id=db.Column(db.Integer)

    def __init__(self,follower_id,following_id,follow_info):
        self.following_id = follower_id
        self.follower_id = following_id
        self.follow_info = follow_info

class UpLoad:
    UPLOAD_FOLDER = 'upload'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    def allowed_file(self,filename):
        ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG'])
        return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    def upload(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        file_dir = os.path.join(basedir,app.config['UPLOAD_FOLDER'])
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        f = request.files['file']
        if f and self.allowed_file(f.filename):
            fname=secure_filename(f.filename)
            ext = fname.rsplit('.', 1)[1]
            unix_time = int(time.time())
            new_filename = str(unix_time)+'.'+ext
            f.save(os.path.join(file_dir, new_filename))
            return True
        return False
class Commnd_Permission():
    db = SQLAlchemy(app)
    def display_post(self,post_id,title,content,publisher_id,post_time,toppost_id,category_id):
        '''
        发布帖子
        :param post_id:
        :param title:
        :param content:
        :param publisher_id:
        :param post_time:
        :param toppost_id:
        :param category_id:
        :return:
        '''
        self.db.session.add(User(post_id,title,content,publisher_id,post_time,toppost_id,category_id))
        self.db.session.commit()
    def attention(self,follower_id,following_id,follow_info):
        '''
        关注
        :return:
        '''
        self.db.session.add(Follow(follower_id,following_id,follow_info))
        self.db.session.commit()
    def display_Category(self,topic_id,category_id):
        self.db.session.add(Follow(category_id,topic_id))
        self.db.session.commit()
