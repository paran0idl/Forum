# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,PasswordField,BooleanField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo

class WriteForm(FlaskForm):
    name = StringField(validators=[Required()])
    text = TextAreaField(validators=[Required()])
    submit = SubmitField(u'发帖')

class CommentForm(FlaskForm):
    text = TextAreaField()
    submit = SubmitField(u'回复')

class DelForm(FlaskForm):
    submit = SubmitField(u'删除')

class LoginForm(FlaskForm):
    email = StringField('Email')
    password = PasswordField('Password',validators=[Required()])
    submit = SubmitField('Log In')

class RegisterForm(FlaskForm):
    email = StringField('Email')
    username = StringField('Username')
    password = PasswordField('Password')
    password2 = PasswordField('Confirm password')
    submit = SubmitField('Register')

class UserInfo(FlaskForm):

    username = StringField('username')

