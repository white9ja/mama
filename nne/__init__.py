import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

import datetime

today = datetime.datetime.now()

app = Flask(__name__)

# app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '9bb2e4c9f4e0d5036e40f575600cf8fa'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/mama2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Create database connection object
# os.environ.get('EMAIL_USER')   
# os.environ.get('EMAIL_PASS')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'cellulantharry@gmail.com'
app.config['MAIL_PASSWORD'] = 'advancegrace201'
mail = Mail(app)


from nne.models import Users, User, Workers, Guarrantor, Payment

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


from nne import routes 