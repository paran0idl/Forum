from flask import render_template, redirect, request, url_for, flash,current_app
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User, Post
from .forms import LoginForm, RegistrationForm, PostForm
from .. import db
from ..token import generate_confirmation_token,confirm_token
from ..email import send_email
from ..models import Category

@auth.route('/login', methods=['GET', 'POST'])
def login():
    category = Category.query.all()
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data).first()
        if user is not None and user.user_pwd == form.password.data:
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form,category=category)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    category = Category.query.all()
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(user_email=form.email.data,
                    user_name=form.username.data,
                    user_pwd=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = generate_confirmation_token(user.user_email)
        send_email(user.user_email, 'Confirm Your Account',
                   'email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form,category=category)



@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.email_confirm == True:
        return redirect(url_for('main.index'))
    print confirm_token(token)
    if current_user.user_email == confirm_token(token):
        current_user.email_confirm = True
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))

@auth.route('/resend',methods=['get','post'])
@login_required
def resend_email():
    user=current_user
    print user.user_name
    token = generate_confirmation_token(user.user_email)
    send_email(user.user_email, 'Confirm Your Account',
               'email/confirm', user=user, token=token)
    return redirect(url_for('main.index'))


@auth.route('/sendPost/<top_id>',methods=['get','post'])
@login_required
def sendPost(top_id):
    category = Category.query.all()
    form = PostForm()
    print current_user.u_id

    if current_user.email_confirm and form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, publisher_id=current_user.u_id,
                    publisher_name=current_user.user_name, toppost_id=top_id,category_id=1)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('auth/sendPost.html', form=form,user=current_user,category=category)