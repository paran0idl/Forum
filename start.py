#coding:utf-8
import json
import time
from datetime import datetime
from flask import Flask,redirect,session,url_for,flash,request
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_login import login_required
from flask_wtf import Form
from wtforms import StringField,SubmitField,TextAreaField,PasswordField,BooleanField
from flask_login import login_user,logout_user,UserMixin,LoginManager
from flask_sqlalchemy import SQLAlchemy
import six  #get_id
import requests
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
'''
test git
'''
#配置文件
app = Flask(__name__)
bootstrap = Bootstrap(app) #初始化Bootstrap

app.config['SECRET_KEY'] = 'hard to guess string' #WTF SRCF保护
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/new'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['PER_PAGE_NUM'] = 5
URL_REGISTER = 'http://222.18.167.207:4000/auth/register'

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'

db = SQLAlchemy(app)

#Form文件

class WriteForm(Form):
    name = StringField(validators=[Required()])
    text = TextAreaField(validators=[Required()])
    submit = SubmitField(u'发帖')

class CommentForm(Form):
    text = TextAreaField()
    submit = SubmitField(u'回复')

class DelForm(Form):
    submit = SubmitField(u'删除')

class LoginForm(Form):
    username = StringField('username')
    password = PasswordField('Password',validators=[Required()])
    submit = SubmitField('Log In')

#数据库
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

#注册表单
class RegisterForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Register')
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#视图函数
@app.route('/register',methods=['get','post'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        print user.email,user.username,user.password
    return render_template('register.html', form=form)


@app.route('/login',methods=['get','post'])
def login():
    uid = session.get('uid') #防止直接切入login网址造成重复登录
    if uid is not None:
        name = User.query.filter_by(uid=uid).first().username
    else:
        name=''
    form = LoginForm()
    if form.validate_on_submit():
        if uid is None:
            user = User.query.filter_by(email=form.username.data).first()
            if user is not None and user.pwd == form.password.data:
                login_user(user)
                session['uid'] = user.uid
                session['permission'] = user.permission
                eid = request.args.get('eid')
                section = request.args.get('section')
                if eid is not None:
                    return redirect(url_for('essay',eid=eid))
                if section is not None:
                    return redirect(url_for('index',section=section))
                return redirect(url_for('index'))
            else:
                flash('Username or Password error!')
        else:
            flash('You have login,Please logout first!')
    return render_template('login.html',form = form,user_name = name)

@app.route('/logout',methods=['get','post'])
@login_required
def logout():
    logout_user()
    session['uid'] = None
    session['permission'] = 0
    return redirect(url_for('index'))

@app.route('/',methods = ['get','post'])
def index():
    email = request.args.get('email')
    #同步数据库
    if email is not None:
        r = requests.get(url='http://222.18.167.207:4000/others')  # 最基本的GET请求
        html = r.text
        js = json.loads(html)
        for i in js['result']:
            if i['email'] == email:
                um = User(username=i['username'], pwd=i['passwordd'], email=i['email'])
                db.session.add(um)
                db.session.commit()
                break

    type = request.args.get('section')
    uid = session.get('uid')
    person = 'http://222.18.167.207:4000'

    if uid is None:
        uname = ''
    else:
        p = User.query.filter_by(uid=uid).first()
        uname = p.username
        person = person + '?email=' + p.email
    #帖子
    if type is not None:
        if type == 'water':
            name = u'灌水区' #4
            etype = 4
        elif type == 'source':
            name = u'资源共享' #3
            etype = 3
        elif type == 'phone':
            name = u'手机' #2
            etype = 2
        elif type == 'chat':
            name = u'站内交流' #1
            etype = 1
        else:
            return redirect(url_for('index'))

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

            user = User.query.filter_by(uid=id).first()
            user.score += 2
            db.session.add(user)
            db.session.commit()
            author_name = user.username
            essay = Essay(title=title,author=id,author_name=author_name,type=etype,essay=body)
            db.session.add(essay)
            db.session.commit()
            form.name.data = ''
            form.text.data = ''
            return redirect(url_for('index',section=type)) #post get重定向

        return render_template('base.html',
                            url_register = URL_REGISTER,
                            person=person,
                            sec=type,
                            page = page,
                            user_name = uname,
                            pagename = name,modal_name = name,
                            hot_post = hot_post,eassy = eassy,form = form)
    #首页
    num = []
    for i in range(1,5):
        num.append(Essay.query.filter_by(type=i).filter_by(visible=True).count())
    hot = Essay.query.filter_by(visible=True).order_by(Essay.visnum.desc()).limit(10)
    return render_template('index.html',
                           url_register=URL_REGISTER,
                           person = person,
                           num = num,
                           user_name = uname,
                           hot = hot)

@app.route('/essay',methods = ['get','post'])
def essay():
    person = 'http://222.18.167.207:4000'
    eid = request.args.get('eid')
    if eid is None:
        return redirect(url_for('error_404'))
    #访问次数
    es = Essay.query.filter_by(eid=eid).filter_by(visible=True).first()
    if es is None:
        return redirect(url_for('error_404'))
    es.visnum += 1
    db.session.add(es)
    db.session.commit()
    es.score = User.query.filter_by(uid=es.author).first().score
    if es is None:
        #返回404错误,文章不存在的情况下
        return redirect(url_for('error_404'))
    id = session.get('uid')
    if id is not None:
        p = User.query.filter_by(uid=id).first()
        user = p.username
        person = person + '?email=' + p.email
    else:
        user = ''
    #发表回复

    form = CommentForm()
    if form.validate_on_submit():
        user = User.query.filter_by(uid=id).first()
        user.score += 1
        db.session.add(user)
        db.session.commit()
        author_name = user.username
        cmt = Comment(body=form.text.data, author=id, essay=eid, author_name=author_name)
        db.session.add(cmt)
        db.session.commit()
        return redirect(url_for('essay',eid=eid))
    page = request.args.get('page', 1)
    page = int(page)
    #获取当前帖子的评论
    pagination = es.comments.filter_by(visible=True).order_by(Comment.time.desc()).paginate(page,
                 per_page=app.config['PER_PAGE_NUM'], error_out=False)
    comments = pagination.items
    try:
        n = 2
        for comment in comments:
            #comment = Comment.query.filter_by(cid=1).first()
            author_id = comment.author
            comment.score = User.query.filter_by(uid=comment.author).first().score
            comment.num = n
            n += 1
            #加载头像
            f = open('static//photo//%s.png' % author_id, 'wb')
            a = Image.query.filter_by(user=1).first()
            f.write(a.img)
            f.close()
    except Exception:
        pass
    return render_template('essay.html',
                           user_name = user,
                           url_register=URL_REGISTER,
                           person=person,
                           essay = es,
                           page = page,
                           comments = comments,
                           form = form
                           )

#提交举报
@app.route('/tip')
def tip():
    eid = request.args.get('essay')
    cid = request.args.get('comment')
    tip = Tip(eid=eid,cid=cid)
    db.session.add(tip)
    try:
        db.session.commit()
    except:
        #重复提交针对同一对象的举报而报错
        db.session.rollback()
        return 'Dealing ......'
    return 'Tip success'

@app.route('/management')
@login_required
def manage():
    can = 0
    type = request.args.get('type')
    uid = session.get('uid')
    user = User.query.filter_by(uid=uid).first()
    username = user.username
    if user.permission == 8:
        can = 1
    if type == 'essay':
        if user.permission > 0X01:
            essay = []
            essay_t = Tip.query.filter_by(deal=False).filter_by(cid=None).all()
            false_essay = Essay.query.filter_by(visible=False).all()
            for i in essay_t:
                essay.append(Essay.query.filter_by(eid=i.eid).first())
            return render_template('mng_essay.html',essay_t=essay,
                                   false_essay=false_essay,
                               user_name=username,can=can)
        return redirect(url_for('error_404'))

    elif type == 'comment':
        if user.permission > 0X01:
            comment = []
            comment_t = Tip.query.filter_by(deal=False).filter_by(eid=None).all()
            for i in comment_t:
                comment.append(Comment.query.filter_by(cid=i.cid).first())
            return render_template('mng_comment.html',comment_t=comment,
                               user_name=username,can=can)
        return redirect(url_for('error_404'))

    else:
        if user.permission == 0X08:
            users = User.query.all()
            return render_template('mng_user.html',user_name=username,users=users)
        return redirect(url_for('error_404'))

@app.route('/mng_user',methods=['get','post'])
def mng_user():
    data = data_to_dict(request.get_data())
    user = User.query.filter_by(uid=data['uid']).first()
    user.username = data['username']
    user.score = data['score']
    user.permission = data['permission']
    db.session.add(user)
    db.session.commit()
    return 'correct',200

@app.route('/mng_essay',methods=['get','post'])
def mng_essay():
    data = data_to_dict(request.get_data()) #eid,visible
    essay = Essay.query.filter_by(eid=data['eid']).first()
    tip = Tip.query.filter_by(eid=data['eid']).first()
    tip.deal = True
    tip.deal_id = session.get('uid')
    if str.lower(data['visible']) == 'false':
        essay.visible = False
    if str.lower(data['visible']) == 'true':
        essay.visible = True
    db.session.add(essay)
    db.session.add(tip)
    db.session.commit()
    return 'correct',200

@app.route('/mng_comment',methods=['get','post'])
def mng_comment():
    data = data_to_dict(request.get_data()) #cid,visible
    comment = Comment.query.filter_by(cid=data['cid']).first()
    tip = Tip.query.filter_by(cid=data['cid']).first()
    tip.deal = True
    tip.deal_id = session.get('uid')
    if str.lower(data['visible']) == 'false':
        comment.visible = False
    if str.lower(data['visible']) == 'true':
        comment.visible = True
    db.session.add(comment)
    db.session.add(tip)
    db.session.commit()
    return 'correct',200

@app.route('/error_404')
def error_404():
    return render_template('error404.html')

#API
@app.route('/phone_get_user')
def phone_get_user():
    try:
        email = request.args.get('email') #1-100 1-100 101->
        user = User.query.filter_by(email=email).first()
        if user is None:
            return 'None'
        dict = {
        'uid':user.uid,
        'username':user.username,
        'email':user.email,
        'pwd':user.pwd,
        'score':user.score,
        'permission':user.permission
    }
        return json.dumps(dict)
    except Exception:
        return 'None'

@app.route('/phone_get_search')
def phone_get_search():
    try:
        essay = request.args.get('essay')
        if essay is not None:
            re = Essay.query.filter_by(visible=True).filter(Essay.title.like('%' + essay + '%')).all()

        email = request.args.get('email')
        if email is not None:
            user = User.query.filter_by(email=email).first()
            re = user.essays.all()

        if re is None:
            return redirect(url_for('error_404'))
        list = []
        length = len(re)
        for i in re:
            dict = {}
            dict['eid'] = i.eid
            dict['visnum'] = i.visnum
            dict['title'] = i.title
            dict['type'] = i.type
            dict['time'] = i.time.strftime("%Y-%m-%d %H:%M:%S")
            dict['author'] = i.author
            dict['author_name'] = i.author_name
            list.append(dict)
        d = {'result': list}
        return json.dumps(d)
    except Exception:
        return 'None'

@app.route('/phone_get_comment')
def phone_get_comment():
    try:
        eid = request.args.get('eid')
        eid = int(eid)
        essay = Essay.query.filter_by(visible=True).filter_by(eid=eid).first()
        if essay is None:
            return 'None'
        comments = essay.comments.filter_by(visible=True).all()
        list = []
        d = {
                'cid': 0,
                'body':essay.essay,
                'time':essay.time.strftime("%Y-%m-%d %H:%M:%S"),
                'author':essay.author,
                'author_name': essay.author_name
            }
        list.append(d)
        for comment in comments:
            dict = {
                'cid': comment.cid,
                'body': comment.body,
                'time': comment.time.strftime("%Y-%m-%d %H:%M:%S"),
                'author': comment.author,
                'author_name': comment.author_name
            }
            list.append(dict)
            dict = {'result': list}
        return json.dumps(dict)
    except Exception:
        return 'None'

@app.route('/phone_post_essay')
def phone_post_essay():
    try:
        author = request.args.get('uid')
        title = request.args.get('title')
        essay = request.args.get('content')
        type = request.args.get('section')
        if author and title and essay and type:
            new = Essay(title=title,author=author,essay=essay,type=type)
            db.session.add(new)
            db.session.commit()
            return '1'
        return '0'
    except Exception:
        return '0'

@app.route('/phone_post_comment')
def phone_post_comment():
    try:
        author = int(request.args.get('uid'))
        author_name = User.query.filter_by(uid=author).first().username
        body = request.args.get('content')
        essay = int(request.args.get('eid'))

        new = Comment(body=body,author=author,essay=essay,author_name=author_name)
        db.session.add(new)
        db.session.commit()
        return '1'
    except Exception:
        return '0'

@app.route('/get_my_code')
def get_my_code():
    return redirect(url_for('static',filename='work.rar'))

@app.route('/get_apk')
def get_apk():
    return redirect(url_for('static',filename='a.apk'))

#将数据转换为字典，举报视图函数使用
def data_to_dict(data):
    ins = data.split('&')
    data = {}
    for i in ins:
        i = i.split('=')
        data[i[0]] = i[1]
    return data

if __name__ == '__main__':
    login_manager.init_app(app)
    app.run('127.0.0.1')
    #app.run(debug=True)