from flask_wtf import Form
from wtforms import BooleanField, TextField, IntegerField, FloatField, SelectField, SelectMultipleField, validators

class SampleForm(Form):
    message = TextField('Message')
