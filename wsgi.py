import os
import json

from app import app, db

configuration_file = os.environ.get('APP_CONFIG_FILE')
app.config['UI'] = json.load(open(configuration_file))
db.init(app.config['UI']['database'])
