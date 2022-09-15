from flask import Flask, request, jsonify, render_template, make_response, redirect
import time
import sqlite3

app = Flask(__name__)

def get_usernames():
	usernames1 = []
	con = sqlite3.connect("data.db")
	cur = con.cursor()
	res = cur.execute("SELECT * FROM users")
	tmp = res.fetchall()
	for i in tmp:
		usernames1.append(i[0])
	return usernames1

global usernames
usernames = get_usernames()



#############



@app.route('/', methods=['GET']) 
def index_page():
	data = get_balance_table()
	return render_template('index.html', data=data)

def get_balance_table():
	con = sqlite3.connect("data.db")
	cur = con.cursor()
	res = cur.execute("SELECT * FROM users")
	tmp = res.fetchall()
	con.close()
	result = '<table><tr><th>user</th><th>balance</th><th>login as</th><tr>'
	for i in tmp:
		result += '<tr><th>' + i[0] + '</th><th>' + i[1] + '</th><th><button type="button" onclick="document.location=\'/login_as?u=' + i[0] + '\'">-&gt;</button></th></tr>' 
	result += '</table>'
	return result


@app.route('/login_as', methods=['GET']) 
def index():
	global usernames
	username = request.args.get('u')
	if username not in usernames:
		return 'invalid username <a href=\'/\'>/</a>'
	else:
		resp = make_response(render_template('redirect_send.html'))
		resp.set_cookie('u', username)
		return resp
	return 'aaaa'#render_template('index.html')

@app.route('/send', methods=['GET']) 
def send_money_page():
	alertnot = ''
	try:
		alertnot = request.args.get('alert')
	except:
		pass
	username = request.cookies.get('u')
	if username not in usernames:
		return 'invalid username <a href=\'/\'>/</a>' 
	con = sqlite3.connect("data.db")
	cur = con.cursor()
	com = "SELECT balance FROM users WHERE username=\'" + username + "\'"
	res = cur.execute(com)
	tmp = res.fetchone()
	con.close()
	balance = str(tmp[0])
	return render_template('send.html', balance=balance, username=username, alertnot=alertnot)

@app.route('/confirm_send', methods=['GET'])
def send_money():
	global usernames
	username = request.cookies.get('u')
	if username not in usernames:
		return 'invalid username <a href=\'/\'>/</a>'
	
	try:
		amount = request.args.get('a')
		amount = int(amount)
		if amount <= 0:
			return 'invalid amount <a href=\'/\'>/</a>'
	except:
		return 'invalid amount <a href=\'/\'>/</a>'
	try:
		receiver = request.args.get('r')
		if receiver not in usernames:
			return 'invalid receiver <a href=\'/\'>/</a>'
	except:
		return 'invalid receiver <a href=\'/\'>/</a>'
	con = sqlite3.connect("data.db")
	cur = con.cursor()
	com = "SELECT balance FROM users WHERE username=\'" + username + "\'"
	res = cur.execute(com)
	tmp = res.fetchone()
	balance = str(tmp[0])
	balance = int(balance)
	if balance - amount < 0:
		return 'not enough balance <a href=\'/\'>/</a>'
	com = "SELECT balance FROM users WHERE username=\'" + receiver + "\'"
	res = cur.execute(com)
	tmp = res.fetchone()
	balance2 = str(tmp[0])
	balance2 = int(balance2)
	user1_balance = balance - amount
	user2_balance = balance2 + amount
	com = "UPDATE users SET balance=\'" + str(user1_balance) + "\' WHERE username=\'" + username + "\'"
	res = cur.execute(com)
	com = "UPDATE users SET balance=\'" + str(user2_balance) + "\' WHERE username=\'" + receiver + "\'"
	res = cur.execute(com)
	con.commit()
	con.close()
	return redirect("/", code=302)

@app.route("/time")
def print_time():
		t_time = str(time.time()) + '\n'     #we can see the time when func was triggered
		return t_time