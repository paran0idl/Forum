# -*- coding: utf-8 -*-
from flask_login import UserMixin
from . import db
import six
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import time

class Permission:
    FOLLOW = 0X01
    ADMIN = 0X04

class Follow(db.Model):
    __tablename__ = 'Follow'
    follower_id = db.Column(db.Integer, db.ForeignKey('user.u_id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.u_id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

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
    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.u_id).first()
        if f:
            db.session.delete(f)

    def is_following(self, user):
        return self.followed.filter_by(followed_id=user.u_id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(follower_id=user.u_id).first() is not None

    def get_id(self):
        try:
            return six.text_type(self.u_id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def publish_post(self,post_id,title,content,publisher_id,post_time,toppost_id,category_id):
        tmp = Post(po_st_id,title,content,publisher_id,post_time,toppost_id,category_id)
        db.session.add(tmp)
        db.session.commit()


class Post(db.Model):
    __tablename__='post'
    post_id=db.Column(db.Integer,primary_key=True,index=True,autoincrement=True)
    title=db.Column(db.UnicodeText)
    content=db.Column(db.UnicodeText)
    publisher_id=db.Column(db.Integer,db.ForeignKey('user.u_id'))
    publisher_name=db.Column(db.String(64))
    post_time=db.Column(db.DateTime, index=True, default=datetime.utcnow)
    toppost_id=db.Column(db.Integer)
    category_id=db.Column(db.Integer)
    post_score=db.Column(db.Integer,default=0)
    publisher_name=db.Column(db.UnicodeText)

    def __init__(self,post_id,title,content,publisher_id,post_time,toppost_id,category_id,publisher_name):
        self.post_id = po_st_id
        self.title = title
        self.content = content
        self.publisher_id = publisher_id
        self.post_time = post_time,
        self.toppost = toppost_id,
        self.category = category_id,
        self.publisher_name=publisher_name

class Category(db.Model):
    __tablename__='category'
    category_id=db.Column(db.Integer,primary_key=True,index=True,autoincrement=True,unique=True)
    topic_id=db.Column(db.Integer)

    def __init__(self,category_id,topic_id):
        self.category_id = category_id
        self.topic_id = topic_id





class UpLoad:
    def allowed_file(self,filename):
        ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG'])
        return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    def upload(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        file_dir = os.path.join(basedir,'upload')
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
