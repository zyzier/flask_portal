#coding utf-8
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from datetime import datetime
from app import app, db, lm
from forms import LoginForm, EditForm, CheckServerForm
from models import User, Post, ROLE_USER, ROLE_ADMIN
#For working with commandline it's better to use subprocesses unlike os module
from subprocess import Popen, PIPE


@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.before_request
def before_request():
	g.user = current_user
	if g.user.is_authenticated():
		g.user.last_seen = datetime.utcnow()
		db.session.add(g.user)
		db.session.commit()

@app.route('/')
@app.route('/index', methods = ['GET', 'POST'])
@login_required
def index():
    user = g.user
    form = CheckServerForm()
    if form.validate_on_submit():
        p = form.password.data
        check_command = Popen(["flask/bin/python", "checkvps.py"], stdout = PIPE, stdin = PIPE)
    	#return check_command.communicate(input = p)[0]
        return render_template("summary.html", output = check_command.communicate(input = p)[0] ) 
    return render_template("index.html", title = 'Home', user = user, form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
    	return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
    	session['remember_me'] = form.remember_me.data 
    	#we can look at data that usr input to our fields
    	#flash('Login requested="' + form.login.data + '", Password="' + form.password.data + '",remember_me=' + str(form.remember_me.data))
        return after_login(form.login.data)
    return render_template('login.html', title = 'Sign In', form = form)

def after_login(nickname):
	user = User.query.filter_by(nickname = nickname).first()
	#check exist or not
	if user is None or user == "":
		flash('Invalid login. Try again.')
		return redirect(url_for('login'))
	remember_me = False
	if 'remember_me' in session:
		remember_me = session['remember_me']
		session.pop('remember_me', None)
	login_user(user, remember = remember_me)
	return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
	user = User.query.filter_by(nickname = nickname).first()
	posts = g.user.posts.all()
	if user == None:
		flash('User: ' + nickname + 'not found.')
		return redirect(url_for('index'))
	return render_template('user.html', user = user, posts = posts)

@app.route('/edit_post_<post_id>', methods = ['GET', 'POST'])
@login_required
def edit(post_id):
        form = EditForm()
	if form.validate_on_submit():
		post = Post.query.get(post_id)
		post.title = form.title.data
		post.body = form.post.data
		post.timestamp = datetime.utcnow()
		db.session.add(post)
		db.session.commit()
		flash('CHANGES SAVED!!!')
		return redirect(url_for('index'))
	else:
		form.post.data = Post.query.get(post_id)
		form.title.data = Post.query.get(post_id).Title()
		return render_template('edit.html', form = form)

#Post view page
@app.route('/post_<post_id>', methods = ['GET'])
@login_required
def view_post(post_id):
	user = g.user
	post = Post.query.get(post_id)
	return render_template('view_post.html', user = user, post = post)

#Try to view XML
#@app.route('/testxml')
#def xml():
#	return render_template('db_visual.xml')

#Error Handlers
@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html')

@app.errorhandler(500)
def internal_error(error):
	return render_template('500.html')
