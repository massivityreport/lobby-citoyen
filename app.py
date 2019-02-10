#! /usr/bin/env python

import json
import argparse
import sys
import traceback
import datetime
from collections import defaultdict

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import abort
from flask import Response

from flask_security import Security
from flask_security import SQLAlchemyUserDatastore
from flask_security import UserMixin
from flask_security import RoleMixin
from flask_security import login_required

from flask_mail import Mail
from flask_mail import Message

from model import db
from model import User
from model import Role

import filters
from forms import *

class FixScriptName(object):
    def __init__(self, app, prefix):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        print(environ['PATH_INFO'])
        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])
            return ["This doesn't get served by your FixScriptName middleware.".encode()]

# Create app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
app.config['SECURITY_PASSWORD_SALT'] = 'scoupon-secret'

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# template filters
app.register_blueprint(filters.blueprint)

# mail
mail = Mail()

@app.route("/")
def home():
    deputes = []
    with open('data/deputes.jsons') as db:
        for d in db:
            deputes.append(json.loads(d))
    text = json.load(open('data/text.json'))
    return render_template('home.html', deputes=deputes, text=text)

@app.route("/send-mail", methods=['POST'])
def send_mail():
    data = request.form
    text = json.load(open('data/text.json'))
    body = 'This is a test mail for %s <%s>' %(
        data['DEST_NAME'], data['DEST_EMAIL']
    )
    message = Message(body, sender=(data['NAME'], data['EMAIL']), recipients=['david@massivityreport.com'])
    mail.send(message)
    print('sent')
    return 'OK'


def build_app(configuration_file):
    app.config['UI'] = json.load(open(configuration_file))
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['UI']['database']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.wsgi_app = FixScriptName(app.wsgi_app, '/laffairedusiecle')
    db.init_app(app)
    mail.init_app(app)
    return app

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the web app')
    parser.add_argument('configuration_file', help='The JSON configuration file')
    args = parser.parse_args()

    # Go !
    app = build_app(args.configuration_file)
    app.run(host=app.config['UI']['host'], port=app.config['UI']['port'], debug=True)
