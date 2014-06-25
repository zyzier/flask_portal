from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length

class LoginForm(Form):
    login = TextField('login', validators = [InputRequired(message = 'Need some login')])
    password = PasswordField('password', validators = [InputRequired(message = 'Need some pass')])
    remember_me = BooleanField('remember_me', default = False)

class EditForm(Form):
	title = TextField('title', validators = [InputRequired(message = 'Need some title'), Length(min = 0, max = 120)])
	post = TextAreaField('post', validators = [Length(min = 0, max = 500)])

class CheckServerForm(Form):
	password = PasswordField('password', validators = [InputRequired(message = 'Need admin pass')])