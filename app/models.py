# -*- coding: utf-8 -*-
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager
import six  #get_id
from datetime import datetime
import os
from werkzeug.utils import secure_filename

class User(UserMixin,db.Model):
    __tablename__='user'
    u_id = db.Column(db.Integer,primary_key=True,index=True,autoincrement=True)
    user_name=db.Column(db.String(64),unique=True)
    user_email=db.Column(db.String(64),unique=True)
    user_pwd=db.Column(db.String(64))
    user_permission=db.Column(db.Integer)
    avatar=db.Column(db.LargeBinary)
    email_confirm=db.Column(db.Boolean)

    post=db.relationship('post',backref='post_author', lazy='dynamic')
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



class post(db.Model):
    __tablename__='post'
    post_id=db.Column(db.Integer,primary_key=True,index=True,autoincrement=True)
    title=db.Column(db.UnicodeText)
    content=db.Column(db.UnicodeText)
    publisher_id=db.Column(db.Integer,db.ForeignKey('user.u_id'))
    post_time=db.Column(db.DateTime, index=True, default=datetime.utcnow)
    toppost_id=db.Column(db.Integer)
    category_id=db.Column(db.Integer)

class category(db.Model):
    __tablename__='category'
    category_id=db.Column(db.Integer,primary_key=True,index=True,autoincrement=True,unique=True)
    topic_id=db.Column(db.Integer)

class follow(db.Model):
    __tablename__='follow'
    following_id=db.Column(db.Integer)
    follower_id=db.Column(db.Integer)

class UpLoad:
    UPLOAD_FOLDER = 'upload'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    def allowed_file(self,filename):
        ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF'])
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

