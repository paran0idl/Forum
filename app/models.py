# -*- coding: utf-8 -*-
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager
import six  #get_id
from datetime import datetime
class Permission:
    FOLLOW = 0X01 #一般用户
    ADMIN = 0X04 #协助管理
    ROOT = 0X08 #管理网站

class User(UserMixin,db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer,primary_key=True,index=True,autoincrement=True)
    username = db.Column(db.String(64),unique=True) #username
    email = db.Column(db.String(64),unique=True) #email
    pwd = db.Column(db.String(64))
    score = db.Column(db.Integer,default=0)

    permission = db.Column(db.Integer, default=Permission.FOLLOW)  # 权限

    #关系
    comments = db.relationship('Comment', backref='cauthor', lazy='dynamic') #每个用户的评论
    essays = db.relationship('Essay', backref='eauthor', lazy='dynamic') #每个用户发表的文章

    def __repr__(self):
        return '<User: %s>' % (self.username)

    def get_id(self):
        try:
            return six.text_type(self.uid)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

class Essay(db.Model):
    __tablename__ = 'essay'
    eid = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(64))
    essay = db.Column(db.String(256))
    type = db.Column(db.Integer)  # 所属版块
    score = 0
    visnum = db.Column(db.Integer,default=0) #点击量

    visible = db.Column(db.Boolean,default=True) #是否可见
    time = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    author = db.Column(db.Integer, db.ForeignKey('user.uid'))
    author_name = db.Column(db.String(36))
    #关系
    comments = db.relationship('Comment', backref='cessay', lazy='dynamic') #每篇文章对应的评论

class Comment(db.Model):
    __tablename__ = 'comment'
    cid = db.Column(db.Integer,primary_key=True,autoincrement=True)
    body = db.Column(db.String(256))

    time = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    visible = db.Column(db.Boolean,default=True) #是否可见
    # 外键
    author = db.Column(db.Integer, db.ForeignKey('user.uid'))
    author_name = db.Column(db.String(36))
    essay = db.Column(db.Integer, db.ForeignKey('essay.eid'))

    score = 0 #不在表内
    num = 0

class Image(db.Model):
    __tablename__ = 'image'
    mid = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.uid'))
    img = db.Column(db.LargeBinary) #二进制

class Tip(db.Model):
    __tablename__ = 'tip'
    tid = db.Column(db.Integer,primary_key=True,index=True)
    eid = db.Column(db.Integer)
    cid = db.Column(db.Integer)
    deal = db.Column(db.Boolean,default=False)
    deal_id = db.Column(db.Integer,default=0)
