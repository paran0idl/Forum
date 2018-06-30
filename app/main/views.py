# -*- coding: utf-8 -*-
from flask import redirect,url_for
from flask import render_template
from app import login_manager
from flask_login import logout_user,current_user,login_required
from . import main
from app.models import User,Post,Follow
from .forms import  RegisterForm,WriteForm
from datetime import datetime

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


@main.route('/',methods = ['get','post'])
def index():
    uid=''
    uname=''
    if not current_user.is_anonymous:
        uid = current_user.u_id
        uname = current_user.user_name
    return render_template('index.html',u_id=uid,user_name=uname)

@main.route('/<u_id>',methods=['get','post'])
@login_required
def user_view(u_id):
    user=User.query.filter_by(u_id=u_id).first()
    following=Follow.query.filter_by(following_id=u_id).all()
    posts=[]
    for f in following:
        for post in Post.query.filter_by(publisher_id=f.following_id).all():
            posts.append(post)
    for post in posts:
        print post.title
    return render_template('index.html',u_id=u_id,user_name=user.user_name,posts=posts)
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
                           
    #return render_template('index.html',user_name=uname)

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

'''

@main.route('/user_center')
@login_required
def user_center():
    name=current_user.user_name
    followed = Follow.query.filter_by(Follow.follower_id == current_user.u_id).first()
    followed_cnt = len(followed)
    fan_cnt = len(Follow.query.filter_by(Follow.followed_id==current_user.u_id).first())
    posts = Post.query.filter_by(Post.publisher_id==current_user.u_id).first()
    return render_template('user_center.html',name=name,followed=followed,followed_cnt=followed_cnt,fan=fan_cnt,posts=posts)

'''
@main.route('/user_info')
@login_required
def user_info():
    form = UserInfo()
    if form.validate_on_submit():
        result = User.query.filter_by(User.user_name == current_user.user_name).first()
        result.user_name=form.username.data
        result.user_pwd=form.newpasswd.data
        result.user_email=form.email.data
        db.session.commit()
        return render_template('index.html')
    return render_template('user_info.html',form=form)
'''

@main.route('/focus')
@login_required
def focus(followed):
    posts = []
    for i in followed:
        post = Post.query.filter_by(Post.publisher_id==i).first()
        posts.append(post)
    return render_template('focus.html',posts=posts)

@main.route('/detail')
@login_required
def detail(post):
    comments = Post.query.filter_by(Post.toppost_id==post.post_id).first()
    return render_template('detail.html', comments=comments,post=post)

@main.route('/detail')
@login_required
def writepost():
    writeform=WriteForm()
    if writeform.validate_on_submit():
        post = Post()
        post.title=writeform.name.data
        post.content=writeform.text.data
        post.publisher_id=current_user.u_id
        post.publisher_name=current_user.user_name
        post.post_time=datetime.now()
        post.toppost_id=0

    return render_template('WritePost.html')
