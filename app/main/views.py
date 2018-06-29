# -*- coding: utf-8 -*-
import json
from flask import Flask,redirect,session,url_for,flash,request
from flask import render_template
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
from app import login_manager
from flask_login import login_user,logout_user
from . import main
from .. import db
from app.models import Permission,User,Essay,Comment,Image,Tip
from .forms import  WriteForm,CommentForm,DelForm,LoginForm,RegisterForm
#import requests
from manage import app
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
URL_REGISTER = 'http://222.18.167.207:4000/auth/register'
#视图函数
@main.route('/register',methods=['get','post'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user_name=User.query.filter_by(username=form.username.data).first()
        new_user_email=User.query.filter_by(email=form.email.data).first()
        if new_user_name!=None and new_user_email!=None:
            flash("User Exist")
        elif form.password.data!=form.password2.data:
            flash("Password not confirmed")
        elif form.username.data=='' or form.email.data=='' or form.password.data=='' or form.password2.data=='':
            flash("Info not complete")
        else:
            new_user=User(username=form.username.data,email=form.email.data,pwd=form.password.data,score=0)
            db.session.add(new_user)
            db.session.commit()
            print ("add user success")
            user= User.query.filter_by(username=form.username.data).first()
            login_user(user)
            session['uid']=user.uid
            session['permission']=user.permission
            return redirect(url_for('main.index'))
    form.username.data = ''
    form.email.data = ''
    form.password.data = ''
    form.password2.data = ''
    return render_template('register.html', form=form,user_name='')

@main.route('/login',methods=['get','post'])
def login():
    uid = session.get('uid') #防止直接切入login网址造成重复登录
    if uid is not None:
        name = User.query.filter_by(uid=uid).first().username
    else:
        name=''
    form = LoginForm()
    if form.validate_on_submit():
        if uid is None:
            print form.username.data
            user = User.query.filter_by(email=form.username.data).first()
            if user is not None and user.pwd == form.password.data:
                login_user(user)
                session['uid'] = user.uid
                session['permission'] = user.permission
                eid = request.args.get('eid')
                section = request.args.get('section')
                if eid is not None:
                    return redirect(url_for('main.essay',eid=eid))
                if section is not None:
                    return redirect(url_for('main.index',section=section))
                return redirect(url_for('main.index'))
            else:
                flash('Username or Password error!')
        else:
            flash('You have login,Please logout first!')
    return render_template('login.html',form = form,user_name = name)

@main.route('/logout',methods=['get','post'])
@login_required
def logout():
    logout_user()
    session['uid'] = None
    session['permission'] = 0
    return redirect(url_for('main.index'))

@main.route('/',methods = ['get','post'])
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
            return redirect(url_for('main.index'))

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
            return redirect(url_for('main.index',section=type)) #post get重定向

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

@main.route('/essay',methods = ['get','post'])
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
        return redirect(url_for('main.essay',eid=eid))
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
@main.route('/tip')
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

@main.route('/management')
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
        return redirect(url_for('main.error_404'))

    else:
        if user.permission == 0X08:
            users = User.query.all()
            return render_template('mng_user.html',user_name=username,users=users)
        return redirect(url_for('main.error_404'))

@main.route('/mng_user',methods=['get','post'])
def mng_user():
    data = data_to_dict(request.get_data())
    user = User.query.filter_by(uid=data['uid']).first()
    user.username = data['username']
    user.score = data['score']
    user.permission = data['permission']
    db.session.add(user)
    db.session.commit()
    return 'correct',200

@main.route('/mng_essay',methods=['get','post'])
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

@main.route('/mng_comment',methods=['get','post'])
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

@main.route('/error_404')
def error_404():
    return render_template('error404.html')

#API
@main.route('/phone_get_user')
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

@main.route('/phone_get_search')
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

@main.route('/phone_get_comment')
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

@main.route('/phone_post_essay')
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

@main.route('/phone_post_comment')
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

@main.route('/get_my_code')
def get_my_code():
    return redirect(url_for('static',filename='work.rar'))

@main.route('/get_apk')
def get_apk():
    return redirect(url_for('static',filename='a.apk'))

@main.route('/user_center')
@login_required
def user_center():
    name=request.args.get('section')
    return render_template('user_center.html',name=name)

@main.route('/user_info')
@login_required
def user_info():
    #name=request.args.get('section')
    return render_template('user_info.html')

@main.route('/focus')
@login_required
def focus():
    #name=request.args.get('section')
    return render_template('focus.html')






#将数据转换为字典，举报视图函数使用
def data_to_dict(data):
    ins = data.split('&')
    data = {}
    for i in ins:
        i = i.split('=')
        data[i[0]] = i[1]
    return data