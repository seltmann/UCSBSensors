from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from app import test
from test import device_ids

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class CSV(FlaskForm):
    d_val = FloatField(label='[1-4]', default=1.0, validators=[DataRequired()])
    t_val = FloatField(label='[1-3]', default=1.0, validators=[DataRequired()])
    for i in device_ids:
        device = BooleanField(label=str(i))
    submit = SubmitField(label='Submit')

