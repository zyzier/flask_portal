from app import db, models

print 'Set username:'
nickname = raw_input()
print 'Set pass for new user:'
password = raw_input()
print 'Set permissions. 0 - is user, 1 - is admin'
role = raw_input()
role = int(role)
print 'Set email for password recovery.'
email = raw_input()

newuser = models.User(nickname = nickname, password = password, role = role, email = email)
db.session.add(newuser)
db.session.commit()
print 'all is ok! User %s added.' % (nickname)
