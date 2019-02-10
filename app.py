#! /usr/bin/env python

import json
import argparse
import sys
import traceback
import datetime
from collections import defaultdict
import pandas as pd

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

from model import db
from model import User
from model import Role

import filters
from forms import *

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

@app.route("/")
def home():
    deputes = pd.read_csv('data/deputes.csv').to_dict('record')
    text = json.load(open('data/text.json'))
    return render_template('home.html', deputes=deputes, text=text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the web app')
    parser.add_argument('configuration_file', help='The JSON configuration file')
    args = parser.parse_args()

    # Go !
    app.config['UI'] = json.load(open(args.configuration_file))
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['UI']['database']
    db.init_app(app)
    app.run(host=app.config['UI']['host'], port=app.config['UI']['port'], debug=True)
