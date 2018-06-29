import os
from app import create_app,db
from flask_migrate import Migrate, MigrateCommand
from app.models import User,Post,Category,Follow

app=create_app(os.getenv('FLASK_CONFIG') or 'default')


if __name__=='__main__':
    app.run('127.0.0.1')