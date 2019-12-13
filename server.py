from flask import Flask, render_template, request, flash, current_app, abort
import psycopg2
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)

app.secret_key = b'\xdd\xd6]j\xb0\xcc\xe3mNF{\x14\xaf\xa7\xb9\x17'


@app.route("/")
def home_page():
    return render_template("homepage.html")


@app.route("/signup")
def sign_up():
    return render_template("signup.html")


@app.route("/signin")
def sign_in():
    return render_template("signin.html")


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
	return render_template("lectures.html", branchnames=branches,day=day,time=time,location=location)


@app.route("/schedule")
def schedule():
    return render_template("schedule.html")


@app.route('/lectures', methods=['POST'])
def lectureregistry():
    names = ["physics", "biology", "chemistry"]
    deneme1 = """"""
    for i in names:
        deneme1 += """<option value="%s">%s</option>""" % (i, i)
    if request.method == "POST":
        car_brand = request.form.get("cars", None)
    return render_template("lectures.html", deneme=deneme1)


@app.route('/', methods=['POST'])
def my_form_post():
	if request.form["btn"] == "Sign Up":
		username = request.form['UserName']
		password = pbkdf2_sha256.hash(request.form['Password'])
		firstname = request.form['FirstName']
		lastname = request.form['LastName']
		title = request.form.getlist('title')
		title = title[0]
		print(title)
		statement = """INSERT INTO Users (username, password, title, name, surname) 
		VALUES ('%s', '%s', '%s', '%s', '%s');""" % (username, password, title, firstname, lastname)
		with psycopg2.connect(
				"""dbname='lsgowduy' user='lsgowduy' host='salt.db.elephantsql.com' 
				password='FbiQok5ytKXzEjdU7MbH46l5AWJbKf3I'""") as connection:
			with connection.cursor() as cursor:
				cursor.execute(statement)
		return render_template("homepage.html")
	elif request.form["btn"] == "Sign In":
		username = request.form['UserName']
		password = request.form['Password']
		statement = """SELECT password from Users WHERE username = '%s'""" % (username,)
		with psycopg2.connect(
				"""dbname='lsgowduy' user='lsgowduy' host='salt.db.elephantsql.com' 
				password='FbiQok5ytKXzEjdU7MbH46l5AWJbKf3I'""") as connection:
			with connection.cursor() as cursor:
				cursor.execute(statement)
				password1 = cursor.fetchone()[0]
				if pbkdf2_sha256.verify(password, password1):
					return render_template("loggedin.html")
				else:
					return """False information! Please try again"""

	return """nothing"""


if __name__ == "__main__":
    app.run()
