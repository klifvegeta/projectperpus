from flask_wtf import Form
from wtforms import TextField, PasswordField, validators, HiddenField, TextAreaField, BooleanField
from wtforms.validators import Required, EqualTo, Optional, Length, Email

class SignupForm(Form):
    email = TextField('Email', validators=[
            Required('Masukkan email yang valid'),
            Length(min=6, message=(u'Email address too short')),
            Email(message=(u'That\'s not a valid email address.'))
            ])
    password = PasswordField('Password', validators=[
            Required(),
            Length(min=6, message=(u'Please give a longer password'))
            ])
    username = TextField('Username', validators=[Required()])
    agree = BooleanField('I agree all your <a href="/static/tos.html">Terms of Services</a>', validators=[Required(u'You must accept our Terms of Service')])

class LoginForm(Form):
    username = TextField('username', validators=[
        Required(),
        validators.Length(min=3, message=(u'your username must be a minimum of 3'))
    ])
    password = PasswordField('password', validators=[
        Required(),
        validators.Length(min=6, message=(u'please give a longer password'))
    ])
    remember_me = BooleanField('remember me', default=False)