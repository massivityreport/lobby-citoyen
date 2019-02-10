#! /usr/bin/env python

import json
import argparse

from app import app
from model import db, User, Role, Monitoring, Campaign
from flask.ext.security import SQLAlchemyUserDatastore


def create_tables():
    db.create_all(app=app)


def create_user():
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    user_datastore.create_user(email='admin', password='admin')
    db.session.commit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the web ui')
    parser.add_argument('configuration_file', help='The JSON configuration file')
    args = parser.parse_args()

    # Go !
    app.config['UI'] = json.load(open(args.configuration_file))
    app.config.update(app.config['UI']['database'])
    db.init_app(app)
    db.app = app
    create_tables()
    create_user()
