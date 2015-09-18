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

#Pagination
POSTS_PER_PAGE = 3

#Additional configuretion
#Transmission web-interface:
TORRENT_WEB_URL = 'http://zyzier.tk:9091/transmission/web/'

#MPD server:
MPD_HOST = "89.223.57.88"
MPD_PORT = 6600

#Upload directory:
UPLOAD_FOLDER = '/home/peps/portal/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
