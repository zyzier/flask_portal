# coding: utf-8
from app import db, bcrypt

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    password = db.Column(db.String(120), index = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    last_seen = db.Column(db.DateTime)
    email = db.Column(db.String(120), index=True, unique=True)

    def __init__(self, nickname, password, role, email):
        self.nickname = nickname
        self.password = bcrypt.generate_password_hash(password)
        self.role = role
        self.email = email

    def is_active(self):
    	return True
    def is_authenticated(self):
    	return True
    def is_anonymous(self):
    	return False
    def get_id(self):
    	return unicode(self.id)
    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120), unique = True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def Title(self):
        return (self.title)

    def __repr__(self):
        #To return text as normal utf8 string need to convert it:
        return unicode(self.body)
