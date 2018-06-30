from flask import redirect,url_for,request
from flask import render_template
from app import login_manager
from flask_login import logout_user,current_user,login_required
from . import main
from app.models import User,Post,Follow

@main.route('/show_post',methods=['get','post'])
def show_post(post_id):
    post=Post.query.filter_by(post_id=post_id).first()
    return render_template('show_post.html', title = post.session.get['title'],
                           content = post.session.get['content'],
                           u_name = post.session.get['publisher_name'],
                           time = post.session.get['post_time'],
                           )
