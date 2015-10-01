from app import db, models, bcrypt

print 'Set username:'
nickname = raw_input()
user = models.User.query.filter_by(nickname='tester').first()
print 'Set new pass for %s:' % user
user.password = bcrypt.generate_password_hash(raw_input())

db.session.commit()
print 'all is ok! '



