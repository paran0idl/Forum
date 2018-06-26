#coding:utf-8
from datetime import datetime
from flask import Flask,render_template,redirect,url_for
from flask_login import login_user,UserMixin,LoginManager
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField,SubmitField,TextAreaField,PasswordField,BooleanField
from wtforms.validators import Required
from flask_bootstrap import Bootstrap
from flask_wtf import Form
import json
import requests

app = Flask(__name__)
bootstrap = Bootstrap(app) #初始化Bootstrap
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'hard to guess string' #WTF SRCF保护
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/new'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'

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
    score = 0
    visnum = db.Column(db.Integer,default=0) #点击量
    type = db.Column(db.Integer)  # 所属版块

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
    img = db.Column(db.LargeBinary)

class Tip(db.Model):
    __tablename__ = 'tip'
    tid = db.Column(db.Integer,primary_key=True,index=True)
    eid = db.Column(db.Integer,unique=True)
    cid = db.Column(db.Integer,unique=True)
    deal = db.Column(db.Boolean,default=False)
    deal_id = db.Column(db.Integer,default=0)

if __name__ == '__main__':
    r = requests.get(url='http://222.18.167.207:4000/others')  # 最基本的GET请求
    html = r.text
    js = json.loads(html)
    user = []
    email = '380850054@qq.com'
    for i in js['result']:
        if i['email'] == email:
            #user = User(username=i['username'],pwd=i['passwordd'],email=i['email'])
            #db.session.add(user)
            #db.session.commit()
            print i
            break
    '''
    eid = 1
    essay = Essay.query.filter_by(visible=True).filter_by(eid=eid).first()
    comments = essay.comments.filter_by(visible=True).all()
    list = []
    for comment in comments:
        dict = {
            'cid':comment.cid,
            'body':comment.body,
            'time':comment.time.strftime("%Y-%m-%d %H:%M:%S"),
            'author':comment.author,
            'author_name':comment.author_name
        }
        list.append(dict)
        dict = {'result':list}
        print json.dumps(dict)
    '''
    '''
    user = User.query.filter_by(email='1105066510@qq.com').first()
    re = user.essays.all()
    dict = {}
    list = []
    for i in range(0, len(re)):
        dict['eid'] = re[i].eid
        dict['visnum'] = re[i].visnum
        dict['type'] = re[i].type
        dict['time'] = re[i].time.strftime("%Y-%m-%d %H:%M:%S")
        dict['author'] = re[i].author
        dict['author_name'] = re[i].author_name
        list.append(dict)
    d = {'result': list}
    print json.dumps(d)
    '''

    '''
    user = User(username='mamao', pwd='admin', email='110965893@qq.com')
    db.session.add(user)
    db.session.commit()
    '''
    '''
    essay = Essay.query.filter_by(eid=1).first()
    print essay.author
    '''
    '''
    db.drop_all()
    db.create_all()

    user = User(username='root',pwd='rrrr',email='1105066510@qq.com')
    essay1 = Essay(title='title1',essay='hanwweibozaizhe',author='1',author_name='root',type=1,visnum=10)
    essay2 = Essay(title='title2',essay='woshihanweibo',author='1',author_name='root',type=1,visnum=10)

    comment1 = Comment(body='我是社会主义接班人',author=1,essay = '1',author_name='root')
    comment2 = Comment(body='是', author=1,essay = '1',author_name='root')

    db.session.add(user)
    db.session.add(essay1)
    db.session.add(essay2)
    db.session.add(comment1)
    db.session.add(comment2)
    db.session.commit()

    img = open('test.png', 'rb').read()
    a = Image(user=1, img=img)
    db.session.add(a)
    db.session.commit()

    #'''
    '''
    comment = Comment.query.filter_by(cid=3).first()
    print comment.body
    #'''

    '''
    f = open('test.png','rb')
    a = f.read()
    f.close()
    f = open('a.jpg','wb')
    f.write(a)
    f.close()
    '''
    '''
    image = Image.query.filter_by(user = 1).first().img
    f = open('a.jpg','wb')
    f.write(image)
    f.close()
    '''
