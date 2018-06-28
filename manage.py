import os
from app import create_app,db
from app.models import User,Essay,Comment,Image,Tip

app=create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__=='__main__':
    app.run('127.0.0.1')