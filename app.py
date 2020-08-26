#run it: gunicorn --worker-class=eventlet app:app
import os
import requests


from flask import Flask, request, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

if __name__ == '__main__':
	socketio.run(app)


class User(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)

	def __repr__(self):
		return f"User('{self.username}'. {self.id})"

@app.route('/', methods=['GET', 'POST'])
def index():
	db.create_all()
	u = request.form.get('username')
	p = request.form.get('password')
	allusers = User.query.all()

	for accounts in allusers:
		if u == accounts.username and p == accounts.password:
			return redirect(url_for('chatroom',username=u))
	return render_template('index.html')


@app.route('/register', methods = ['GET', 'POST'])
def register():
	allusers = User.query.all()
	u = request.form.get('username')
	p = request.form.get('password')
	if request.method == "POST":
		if u == None:
			return render_template('register.html', message='Please Enter A Username.')
		if p == None:
			return render_template('register.html', message='Please Enter A Password')
		if p == None and u == None:
			return render_template('register.html', message='Please Enter A Username and Password.')
		for accounts in allusers:
			if u == accounts.username:
				return render_template('register.html', message='Username in use already. Please try another username.')
		db.create_all()
		p = User(username = u, password = p)
		db.session.add(p)
		db.session.commit()
		print(User.query.all())
		return render_template('index.html')
	return render_template('register.html')


@app.route('/accounts')
def showaccounts():
	arr = []
	allusers = User.query.all()
	
	for accounts in allusers:
		arr.append([accounts.username, accounts.password])
	return render_template('accounts.html', users = arr)

@app.route('/chatroom/<username>')
def chatroom(username):
	return render_template('urin.html', u=username)


@socketio.on("messagesent")
def broadcastmessage(data):
	pmessage = data["message"];
	emit("finalmessage", {'message':pmessage}, broadcast="True")






