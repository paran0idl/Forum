from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

bootstrap = Bootstrap()

'''
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/new'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['PER_PAGE_NUM'] = 5
URL_REGISTER = 'http://222.18.167.207:4000/auth/register'
'''
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['PER_PAGE_NUM'] = 5
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/new'
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import  main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
'''
if __name__ == '__main__':
    login_manager.init_app(app)
    app.run('127.0.0.1')
    #app.run(debug=True)
'''