# import the necessary packages
from flask import Flask, render_template, redirect, url_for, request,session,Response
from werkzeug import secure_filename
import sqlite3
import pandas as pd
from datetime import datetime
from utils import *
import os
import cv2
import playsound
import random
from notification import *
from firebaseUpload import *



name = ''
username = ''
password = ''
upassword = ''
lockerid = ''
email = ''
name = ''
lname = ''
otp = ''
count = 0
fingerID = 0

app = Flask(__name__)

app.secret_key = '1234'
app.config["CACHE_TYPE"] = "null"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/', methods=['GET', 'POST'])
def landing():
	return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	global name
	global count
	global otp
	global fingerID
	if request.method == 'POST':
		fingerID = searchFinger()
		print(fingerID)
		if(fingerID == -1):
			count = count + 1
			if(count == 3):
				playsound.playsound('alarm.wav')
				count = 0
			return render_template('login.html',error="FingerPrint Not Matched")
		elif(fingerID == -2):
			return render_template('login.html',error="Problem with FingerPrint Sensor")
		else:
			con = sqlite3.connect('mydatabase.db')
			cursorObj = con.cursor()
			cursorObj.execute(f"SELECT Name from Account WHERE FingerID='{fingerID}';")
			try:
				name = cursorObj.fetchone()[0]
				print('name=',name)
				count = 0
				otp = random.randint(1000,9999)
				print(otp)
				pushbullet_noti("OTP",str(otp))
				
				return redirect(url_for('otp'))
			except:
				error = "No Account Found..!!!"
				count = count + 1
				return render_template('login.html',error=error)

		'''
		email = request.form['email']
		password = request.form['password']
		con = sqlite3.connect('mydatabase.db')
		cursorObj = con.cursor()
		cursorObj.execute(f"SELECT Name from Users WHERE Email='{email}' AND password = '{password}';")
		try:
			name = cursorObj.fetchone()[0]
			if('admin' in name):
				return redirect(url_for('home1'))
			else:
				return redirect(url_for('home1'))
		except:
			error = "Invalid Credentials Please try again..!!!"
			return render_template('login.html',error=error)
		'''
	return render_template('login.html')

@app.route('/otp', methods=['GET', 'POST'])
def otp():
	global name
	global otp
	if request.method=='POST':
		otp1 = int(request.form['otp'])
		if(otp == otp1):
			writeFirebase(fingerID)
			return redirect(url_for('home'))
		else:
			writeFirebase(-1)
			return redirect(url_for('login'))
	return render_template('login1.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	error = None
	if request.method == 'POST':
		if request.form['sub']=='Submit':
			name = request.form['name']
			email = request.form['email']
			password = request.form['password']
			rpassword = request.form['rpassword']
			pet = request.form['pet']
			if(password != rpassword):
				error='Password dose not match..!!!'
				return render_template('register.html',error=error)
			try:
				con = sqlite3.connect('mydatabase.db')
				cursorObj = con.cursor()
				cursorObj.execute(f"SELECT Name from Users WHERE Email='{email}' AND password = '{password}';")
			
				if(cursorObj.fetchone()):
					error = "User already Registered...!!!"
					return render_template('register.html',error=error)
			except:
				pass
			now = datetime.now()
			dt_string = now.strftime("%d/%m/%Y %H:%M:%S")			
			con = sqlite3.connect('mydatabase.db')
			cursorObj = con.cursor()
			cursorObj.execute("CREATE TABLE IF NOT EXISTS Users (Date text,Name text,Email text,password text,pet text)")
			cursorObj.execute("INSERT INTO Users VALUES(?,?,?,?,?)",(dt_string,name,email,password,pet))
			con.commit()

			return redirect(url_for('login'))

	return render_template('register.html')

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
	error = None
	global name
	if request.method == 'POST':
		email = request.form['email']
		pet = request.form['pet']
		con = sqlite3.connect('mydatabase.db')
		cursorObj = con.cursor()
		cursorObj.execute(f"SELECT password from Users WHERE Email='{email}' AND pet = '{pet}';")
		
		try:
			password = cursorObj.fetchone()
			#print(password)
			error = "Your password : "+password[0]
		except:
			error = "Invalid information Please try again..!!!"
		return render_template('forgot-password.html',error=error)
	return render_template('forgot-password.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
	global name
	return render_template('home.html',name=name)

@app.route('/home1', methods=['GET', 'POST'])
def home1():
	global name
	global otp
	otp = randint(1000,9999)
	pushbullet_noti('OTP',otp)
	print("OTP:",otp)
	return render_template('home1.html',name=name)
'''
@app.route('/uregister', methods=['GET', 'POST'])
def uregister():
	global username
	global password
	global upassword
	global lockerid
	global email
	global name
	global lname
	error = ""

	if request.method=='POST':
		username = request.form['name']
		email = request.form['email']
		password = request.form['password']
		upassword = request.form['upassword']
		lockerid = request.form['lockerid']
		lname = request.form['lname']

		con = sqlite3.connect('mydatabase.db')
		cursorObj = con.cursor()
		cursorObj.execute(f"SELECT Name from Users WHERE Email='{email}' AND password = '{password}';")
		try:
			name = cursorObj.fetchone()[0]
			return redirect(url_for('register1'))
		except:
			error = "Invalid Credentials Please try again..!!!"
			return render_template('uregister.html',error=error,name=name)		
	return render_template('uregister.html',error=error,name=name)

@app.route('/register1', methods=['GET', 'POST'])
def register1():
	global username
	global password
	global upassword
	global lockerid
	global email
	global name
	
	if request.method=='POST':

		username = request.form['name']
		password = request.form['upassword']

		con = sqlite3.connect('mydatabase.db')
		cursorObj = con.cursor()
		cursorObj.execute("CREATE TABLE IF NOT EXISTS customer (UserName text,Password text)")
		cursorObj.execute("INSERT INTO customer VALUES(?,?)",(username,password))
		con.commit()

		img = cv2.imread('static/img/test_image.jpg')
		cv2.imwrite('dataset/'+username+'.jpg', img)

		return redirect(url_for('uregister'))

	return render_template('register1.html',name=username,lname=lname,password= password,email=email,upassword=upassword,lockerid=lockerid)
'''

@app.route('/ulogin', methods=['GET', 'POST'])
def ulogin():
	global username
	global password
	global name
	global upassword
	global lockerid
	global lname
	global otp
	error = "Put Your Finger on Sensor..!!!"

	if request.method=='POST':
		username = request.form['name']
		print(username)
		#password = request.form['password']
		#upassword = request.form['upassword']
		#lockerid = request.form['lockerid']
		#lname = request.form['lname']

		if(otp == int(username)):
			return redirect(url_for('locker'))
		else:
			error = "Invalid Credentials Please try again..!!!"

		'''
		con = sqlite3.connect('mydatabase.db')
		cursorObj = con.cursor()
		cursorObj.execute(f"SELECT UserName from customer WHERE UserName='{username}' AND password = '{upassword}';")
	
		if(cursorObj.fetchone()):
			return redirect(url_for('login1'))
		else:
			error = "Invalid Credentials Please try again..!!!"
		'''
	return render_template('ulogin.html',error=error,name=name)


@app.route('/locker')
def locker():
	global username
	global name
	global lname
	global lockerid
	#sendSerial(b'O')
	return render_template('locker.html',name=username,lname=lname,lockerid=lockerid)


@app.route('/video_stream')
def video_stream():
	 return Response(video_feed(),mimetype='multipart/x-mixed-replace; boundary=frame')

# No caching at all for API endpoints.
@app.after_request
def add_header(response):
	# response.cache_control.no_store = True
	response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
	response.headers['Pragma'] = 'no-cache'
	response.headers['Expires'] = '-1'
	return response


if __name__ == '__main__' and run:
	app.run(host='0.0.0.0', debug=False, threaded=True)
