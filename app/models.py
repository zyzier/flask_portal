# coding: utf-8
from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    password = db.Column(db.String(120), index = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    last_seen = db.Column(db.DateTime)

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
    body = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def Title(self):
        return (self.title)

    def __repr__(self):
        return (self.body)
        #return '<Post %r' % (self.body)