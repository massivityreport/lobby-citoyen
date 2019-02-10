import os
import json

from app import build_app

configuration_file = os.environ.get('APP_CONFIG_FILE')
app = build_app(configuration_file)
print('starting')
