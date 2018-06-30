from flask import redirect,url_for,request
from flask import render_template
from app import login_manager
from flask_login import logout_user,current_user,login_required
from . import main
from app.models import User,Post,Follow
from .forms import  RegisterForm

@main.route('/register',methods=['get','post'])
def register():
    form = RegisterForm()
    return render_template('register.html', form=form)