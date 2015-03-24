import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'very-secret-key-!@$%^'

SQLALCHEMY_DATABASE_URI = 'mysql://flask@localhost/flaskBD'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

#Mail server settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

#Admins list
ADMINS = ['peps@zyzier.tk', 'pepsbox@gmail.com']