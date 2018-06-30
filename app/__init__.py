from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_mail import Mail
from flask_admin import Admin
from controllers.admin import CustomView

bootstrap = Bootstrap()
mail = Mail()
admin = Admin()

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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/forum'
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    admin.init_app(app)
    admin.add_view(CustomView(name='Custom'))

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