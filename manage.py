import os
from app import create_app,db, admin
from app.controllers.admin import CustomModelView
from app.models import User,Post,Category,Follow

app=create_app(os.getenv('FLASK_CONFIG') or 'default')
models = [User, Post, Category, Follow]
for model in models:
    admin.add_view(
    CustomModelView(model, db.session, category='Models'))

if __name__=='__main__':
    app.run('127.0.0.1')

