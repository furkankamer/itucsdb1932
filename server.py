from flask import Flask, render_template, request, flash, current_app, abort, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import psycopg2
from passlib.hash import pbkdf2_sha256
from user import get_user

app = Flask(__name__)

app.secret_key = b'\xdd\xd6]j\xb0\xcc\xe3mNF{\x14\xaf\xa7\xb9\x17'

lm = LoginManager()

url = "dbname='lsgowduy' user='lsgowduy' host='salt.db.elephantsql.com' password='FbiQok5ytKXzEjdU7MbH46l5AWJbKf3I'"


@lm.user_loader
def load_user(user_id):
    return get_user(user_id)


@app.route("/login", methods=['GET', 'POST'])
def login():
    username = request.form['UserName']
    user = get_user(username)
    if user is not None:
        password = request.form['Password']
        password1 = user.password
        if pbkdf2_sha256.verify(password, password1):
            login_user(user)
            flash("You have logged in.")
            return redirect("/")
    return render_template("signin.html", message="Invalid credentials.")


@login_required
@app.route("/logout")
def logout():
    logout_user()
    return render_template("homepage.html", message="You have logged out.")


@app.route("/")
def home_page():
    return render_template("homepage.html")


@app.route("/signup")
def sign_up():
    return render_template("signup.html")


@app.route("/signin")
def sign_in():
    return render_template("signin.html")


@app.route("/profile")
def profile():
    titles = """select title from users where username = '%s'""" % current_user.username
    with psycopg2.connect(url) as connection:
        with connection.cursor() as cursor:
            cursor.execute(titles)
            title = cursor.fetchone()[0]
            title += """s"""
            statement = """ select*from %s where user_id = (select id from users where username = '%s')""" \
                        % (title, current_user.username)
            cursor.execute(statement)
            for row in cursor.fetchall():
                print(row)
                name = row[1]
                sname = row[2]
                jdate = row[4]
    return render_template("profile.html",
                           otherinf="""""", uname=current_user.username, fname=name, lname=sname, joindate=jdate)


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
    statement = """SELECT title FROM Users WHERE username = '%s'""" % (current_user.username,)
    with psycopg2.connect(url) as connection:
        with connection.cursor() as cursor:
            cursor.execute(statement)
            title = cursor.fetchone()[0]
            if title == "Manager":
                message = "Managers don't have a schedule."
                return render_template("homepage.html", message=message)
            others = title
            others += "s"
            statement = """SELECT name, crn, time, weekday, location_id, quota FROM Lectures WHERE id = (
            SELECT lecture_id FROM %s WHERE user_id = (SELECT id FROM Users WHERE username = '%s'))""" \
                        % (others, current_user.username)
            cursor.execute(statement)
            name = ""
            crn = 0
            time = '00:00'
            weekday = ""
            location_id = 0
            quota = 0
            for row in cursor.fetchall():
                print(row)
                name = row[0]
                crn = row[1]
                time = row[2]
                weekday = row[3]
                location_id = row[4]
                quota = row[5]
            statement = """SELECT name FROM Buildings WHERE id = %s""" % (location_id,)
            cursor.execute(statement)
            location = ""
            for row in cursor.fetchall():
                print(row)
                location = row[0]
            return render_template("schedule.html",
                                   name=name, crn=crn, time=time, weekday=weekday, location=location, quota=quota)


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
    with psycopg2.connect(url) as connection:
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
    with psycopg2.connect(url) as connection:
        with connection.cursor() as cursor:
            cursor.execute(statement)
            return render_template("homepage.html")


lm.init_app(app)
lm.login_view = "login"

if __name__ == "__main__":
    app.run()
