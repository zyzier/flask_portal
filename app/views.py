#coding utf-8
from flask import render_template, flash, redirect, session, url_for, request, g, send_from_directory
from flask.ext.login import login_user, logout_user, current_user, login_required
from datetime import datetime
from app import app, db, lm
from forms import LoginForm, EditForm
from models import User, Post, ROLE_USER, ROLE_ADMIN, bcrypt
#For working with commandline it's better to use subprocesses unlike os module
from subprocess import Popen, PIPE
from config import POSTS_PER_PAGE, MPD_HOST, MPD_PORT, TORRENT_WEB_URL, UPLOAD_FOLDER, ALLOWED_EXTENSIONS

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

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@app.route('/index/<int:page>', methods = ['GET', 'POST'])
@login_required
def index(page = 1):
    user = g.user
    #Using Pagination for regulation posts per page
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template("index.html", title = 'Home', user = user, posts = posts)

###################
## Login process ##
###################

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
    	return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
    	session['remember_me'] = form.remember_me.data 
    	#we can look at data that usr input to our fields:
    	#flash('Login requested="' + form.login.data + '", Password="' + form.password.data + '",remember_me=' + str(form.remember_me.data))
    	#or we can look at headers in request:
    	#flash(str(request.headers))
        return after_login(form.login.data, form.password.data)
    return render_template('login.html', title = 'Sign In', form = form)

def after_login(nickname, password):
	user = User.query.filter_by(nickname = nickname).first()
	if user is not None and bcrypt.check_password_hash(user.password, password):
		remember_me = False
		if 'remember_me' in session:
			remember_me = session['remember_me']
			session.pop('remember_me', None)
			login_user(user, remember = remember_me)
	else:
		flash('Invalid login. Try again.')
		return redirect(url_for('login'))
	return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

##########
## WEED ##
##########

@app.route('/shop', methods = ['GET', 'POST'])
def shop():
	return render_template("shop.html")

###########
## FILES ##
###########

@app.route('/files', methods = ['GET', 'POST'])
@login_required
def files():	
	if request.method == 'POST':
		if 'upload' in request.form and request.files['file']:
			upload_file()
			return redirect(url_for('files'))
		if 'delete' in request.form and request.form.getlist("checked") != []:
			from os import remove, path
			to_delete = request.form.getlist("checked")
			flash('deleting selected files')
			for name in to_delete:
				remove(path.join(UPLOAD_FOLDER, name))
			return redirect(url_for('files'))
		if 'download' in request.form and request.form.getlist("checked") != []:
			to_download = request.form.getlist("checked")
			#for name in to_download:
			#	print name
			return redirect(url_for('download', filename=to_download[0]))
		return redirect(url_for('files'))
	from os import listdir
	filelist = listdir(UPLOAD_FOLDER)
	return render_template('files.html', filelist = filelist)

#Filter for uploading files
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_file_params(filename):
	from os import path
	filepath = path.abspath(UPLOAD_FOLDER) +"/"+ filename
	if path.isfile(filepath):
		return filename, "/download/"+filename, path.getsize(filepath)
	return filename, "/download/"+filename, path.getsize(filepath)

def upload_file():
	file = request.files['file']
	if not allowed_file(file.filename):
		flash('Wrong file type...')
		return redirect(url_for('files'))
	if file and allowed_file(file.filename):
		from os import path
		file.save(path.join(UPLOAD_FOLDER, file.filename))
		return redirect(url_for('files'))
	return redirect(url_for('files'))

@app.route('/files/<path:filename>', methods=['GET', 'POST'])
def download(filename):
	return send_from_directory(directory=UPLOAD_FOLDER, filename=filename)

#################
## System info ##
#################

@app.route('/summary', methods = ['GET'])
@login_required
def summary():
    if g.user.role == 1 :
        out, err = Popen(["flask/bin/python", "checkvps.py"], stdout = PIPE).communicate()
        return render_template("summary.html", output = out)
    return redirect(url_for('index'))           

################
## Tools page ##
################

@app.route('/tools', methods = ['GET'])
#@login_required
def tools():
	return render_template("tools.html")

################
## User page  ##
################

@app.route('/user', methods = ['GET'])
@login_required
def user():
    user = g.user
    return render_template("user.html", user = user)

##############
## Fail2Ban ##
##############

@app.route('/fail2ban', methods = ['GET', 'POST'])
@login_required
def fail2ban():
	if g.user.role == 1:
		#Satus check
		cmd1 = Popen(["sudo", "service", "fail2ban", "status"], stdout = PIPE)
		status = Popen(['sed', '-n', 's/Active://p'], stdin = cmd1.stdout, stdout = PIPE).communicate()
		#Find banned IPs and making tuple
		sedlog = Popen(["sudo", "cat", "/etc/fail2ban/dirty.list"], stdout=PIPE).communicate()
		#Making list from tuple item (string)
		bannedlist = sedlog[0].split("\n")
		#Removing last empty element from string
		bannedlist = bannedlist[:-1]
		return render_template("f2b.html", status = status[0], banned = set(bannedlist))
	return redirect(url_for('index'))

@app.route('/fail2ban/start', methods = ['GET', 'POST'])
@login_required
def f2bstart():
	if g.user.role == 1:
		cmd = Popen(["sudo", "service", "fail2ban", "start"], stdout = PIPE)
		return redirect(url_for('fail2ban'))
	return redirect(url_for('index'))

@app.route('/fail2ban/stop', methods = ['GET', 'POST'])
@login_required
def f2bstop():
	if g.user.role == 1:
		cmd = Popen(["sudo", "service", "fail2ban", "stop"], stdout = PIPE)
		return redirect(url_for('fail2ban'))
	return redirect(url_for('index'))

###########
## NOTES ##
###########

@app.route('/notes', methods = ['GET'])
@app.route('/notes/<int:page>', methods = ['GET'])
@login_required
def notes(page = 1):
	user = g.user
	posts = g.user.posts.paginate(page, 12, False) #12 - post's count on page
	if user == None:
		flash('User: ' + nickname + 'not found.')
		return redirect(url_for('index'))
	#Checking next post_id before creating one
	#in template there is button that uses newpost()
	newpost_id = 1
	for i in Post.query.all():
		if i.id == newpost_id:
			newpost_id += 1
	return render_template('notes.html', user = user, posts = posts, newpost_id = newpost_id)

#Creating post by new post_id with empty body 
def newpost(post_id):
	user = g.user
	post = Post(id = post_id, title = "Some title", timestamp = datetime.utcnow(), author = user)
	db.session.add(post)
	db.session.commit()
	#flash('New post %s created!') % post.id

def deletepost(post_id):
	p = Post.query.get(post_id)
	db.session.delete(p)
	db.session.commit()
	return flash('Post deleted!')

####################
## Post edit page ##
####################
@app.route('/edit_post_<post_id>', methods = ['GET', 'POST'])
@login_required
def edit(post_id):
	user = g.user
	#Creating post before editinf if it's new  
	if not Post.query.get(post_id):
		newpost(post_id)
	post = Post.query.get(post_id)	
	if user != post.author:
		flash('Access denied')
		return redirect(url_for('index'))
        form = EditForm(post.title)
	if form.validate_on_submit():
		#Check what button is pressed
		if 'save' in request.form:
			post = Post.query.get(post_id)
			post.title = form.title.data
			post.body = form.post.data
			post.timestamp = datetime.utcnow()
			db.session.add(post)
			db.session.commit()
			flash('CHANGES SAVED!!!')
			return redirect(url_for('index'))
		elif 'delete' in request.form:
			deletepost(post_id)
			return redirect(url_for('notes'))
	else:
		form.post.data = Post.query.get(post_id)
		form.title.data = Post.query.get(post_id).Title()
		return render_template('edit.html', form = form)

####################
## Post view page ##
####################
@app.route('/post_<post_id>', methods = ['GET'])
@login_required
def view_post(post_id):
	user = g.user
	post = Post.query.get(post_id)
	return render_template('view_post.html', user = user, post = post)

######################
## MPD control page ##
######################
@app.route('/radio', methods = ['GET', 'POST'])
@login_required
def radio():
	import mpd
	try:
		client = mpd.MPDClient()
		client.connect(MPD_HOST, MPD_PORT, timeout = 60)
		onair = client.currentsong()
	except:
		flash('NO MPD CONNeCT!!!!')
		return redirect(url_for('index'))
	if request.method == 'POST':
		if 'next' in request.form:
			client.next()
			return redirect(url_for('radio'))
		elif 'prev' in request.form:
			client.previous()
			return redirect(url_for('radio'))
	return render_template('radio.html', song = onair)

###################
## Filters and   ##
## ErrorHandlers ##
###################

#1.Markdown. For using in template just add {{data|markdown}}
@app.template_filter('markdown')
def markdown_filter(data):
	from flask import Markup
	from markdown2 import markdown
	return Markup(markdown(data))

#2.MPD no tag cheking.
@app.template_filter('no_tag')
def no_tag(song):
	try:
		artist = song['artist'].decode('utf-8')
		title = song['title'].decode('utf-8')
		return artist + ' - ' + title
	except:
		return 'NO TAG'

#Error Handlers
@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html')

@app.errorhandler(500)
def internal_error(error):
	return render_template('500.html')
