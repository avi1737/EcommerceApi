from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate

file_path = os.path.abspath(os.getcwd())+"\info.db"

app = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': 'mh03@u1737',
    'db': 'EcommerceStore',
    'host': 'localhost',
    'port': '5432',
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
'''app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path'''
app.config['SECRET_KEY'] = ""
app.config['SECURITY_PASSWORD_SALT'] = "one side boss"

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'avinashvarpeti1@gmail.com'
app.config['MAIL_PASSWORD'] = 'allineedismoney'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from Projectapi import Routes