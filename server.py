from flask import Flask, render_template, request, flash, current_app, abort, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
import psycopg2
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)

app.secret_key = b'\xdd\xd6]j\xb0\xcc\xe3mNF{\x14\xaf\xa7\xb9\x17'

lm = LoginManager()




@lm.user_loader
def load_user(user_id):
	user = user_id
	statement = """SELECT username, password from Users WHERE username = '%s'""" % (user_id,)
	with psycopg2.connect(
			"""dbname='lsgowduy' user='lsgowduy' host='salt.db.elephantsql.com' 
			password='FbiQok5ytKXzEjdU7MbH46l5AWJbKf3I'""") as connection:
		with connection.cursor() as cursor:
			cursor.execute(statement)
			user = cursor.fetchone()[0]
			if user is not None:
				return user
	return None


@app.route("/login", methods=['GET', 'POST'])
def login():
	username = request.form['UserName']
	statement = """SELECT username from Users WHERE username = '%s'""" % (username,)
	user = username
	with psycopg2.connect(
			"""dbname='lsgowduy' user='lsgowduy' host='salt.db.elephantsql.com' 
			password='FbiQok5ytKXzEjdU7MbH46l5AWJbKf3I'""") as connection:
		with connection.cursor() as cursor:
			cursor.execute(statement)
			user = cursor.fetchone()[0]
	if user is not None:
		password = request.form['Password']
		statement = """SELECT password from Users WHERE username = '%s'""" % (username,)
		with psycopg2.connect(
				"""dbname='lsgowduy' user='lsgowduy' host='salt.db.elephantsql.com' 
				password='FbiQok5ytKXzEjdU7MbH46l5AWJbKf3I'""") as connection:
			with connection.cursor() as cursor:
				cursor.execute(statement)
				password1 = cursor.fetchone()[0]
				if pbkdf2_sha256.verify(password, password1):
					login_user(user)
					flash("You have logged in.")
					return render_template("homepage.html")
	else:
		flash("Invalid credentials.")
	return render_template("signin.html")


@app.route("/logout")
def logout():
	logout_user()
	flash("You have logged out.")
	return render_template("homepage.html")


@app.route("/")
def home_page():
	return render_template("homepage.html")


@app.route("/signup")
def sign_up():
	return render_template("signup.html")


@app.route("/signin")
def sign_in():
	return render_template("signin.html")


@login_required
@app.route("/lectures")
def lectures():
	names = ["Physics", "Biology", "Chemistry"]
	days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
	times = ["9:30", "11:30", "13:30", "15:30"]
	locations = ["MED A34", "EHB 2101", "MDB 105"]
	branches = """"""
	day = """"""
	time = """"""
	location = """"""
	for i in names:
		branches += """<option value="%s">%s</option>""" % (i, i)
	for i in days:
		day += """<option value="%s">%s</option>""" % (i, i)
	for i in times:
		time += """<option value="%s">%s</option>""" % (i, i)
	for i in locations:
		location += """<option value="%s">%s</option>""" % (i, i)
	return render_template("lectures.html", branchnames=branches, day=day, time=time, location=location)


@login_required
@app.route("/schedule")
def schedule():
	return render_template("schedule.html")


@login_required
@app.route('/lectures', methods=['POST'])
def lectureregistry():
	names = ["physics", "biology", "chemistry"]
	deneme1 = """"""
	for i in names:
		deneme1 += """<option value="%s">%s</option>""" % (i, i)
	if request.method == "POST":
		car_brand = request.form.get("cars", None)
	return render_template("lectures.html", deneme=deneme1)


@app.route('/signup', methods=['POST'])
def my_form_post():
	username = request.form['UserName']
	password = pbkdf2_sha256.hash(request.form['Password'])
	firstname = request.form['FirstName']
	lastname = request.form['LastName']
	title = request.form.getlist('title')
	title = title[0]
	userid = 0
	statement = """INSERT INTO Users (username, password, title, name, surname)
	VALUES ('%s', '%s', '%s', '%s', '%s');""" % (username, password, title, firstname, lastname)
	statement += """select id from users where username = '%s'""" % (username)
	with psycopg2.connect(
			"""dbname='lsgowduy' user='lsgowduy' host='salt.db.elephantsql.com'
			password='FbiQok5ytKXzEjdU7MbH46l5AWJbKf3I'""") as connection:
		with connection.cursor() as cursor:
			cursor.execute(statement)
			userid += cursor.fetchone()[0]
	statement = """"""
	if title == "Student":
		degree = request.form['Degree']
		statement += """INSERT INTO Students (name,surname,degree,grade,user_id)
		VALUES ('%s', '%s', '%s', NULL,'%s');""" % (firstname, lastname, degree, userid)
	if title == "Teacher":
		print(request.form)
		experience_year = request.form['Experience']
		subject = request.form['subject']
		statement += """INSERT INTO Teachers (name,surname,subject,experience_year,user_id)
		VALUES ('%s', '%s', '%s', '%s','%s');""" % (firstname, lastname, subject, experience_year, userid)
	if title == "Manager":
		experience_year = request.form['Experience']
		print(experience_year)
		statement += """INSERT INTO Managers (name,surname,user_id,experience_year)
		VALUES ('%s', '%s', '%s', '%s');""" % (firstname, lastname, userid, experience_year)
	with psycopg2.connect(
			"""dbname='lsgowduy' user='lsgowduy' host='salt.db.elephantsql.com' 
			password='FbiQok5ytKXzEjdU7MbH46l5AWJbKf3I'""") as connection:
		with connection.cursor() as cursor:
			cursor.execute(statement)
			return render_template("homepage.html")


lm.init_app(app)
lm.login_view = "login"

if __name__ == "__main__":
	app.run()
