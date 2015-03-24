from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length
from app.models import Post

class LoginForm(Form):
    login = TextField('login', validators = [InputRequired(message = 'Need some login')])
    password = PasswordField('password', validators = [InputRequired(message = 'Need some pass')])
    remember_me = BooleanField('remember_me', default = False)

class EditForm(Form):
	title = TextField('title', validators = [InputRequired(message = 'Need some title'), Length(min = 0, max = 120)])
	post = TextAreaField('post', validators = [InputRequired(message = 'Some message for people?')])
	
	#Adding uniq title check
	def __init__(self, original_title, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		self.original_title = original_title
	def validate(self):
		if not Form.validate(self):
			return False
		if self.title.data == self.original_title:
			return True
		title = Post.query.filter_by(title = self.title.data).first()
		if title != None:
			self.title.errors.append('This title is in use. Use fantasy Bro!')
			return False
		return True

class CheckServerForm(Form):
	password = PasswordField('password', validators = [InputRequired(message = 'Need admin pass')])
