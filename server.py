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
    deneme1 = """"""
    for i in names:
        deneme1 += """<option value="%s">%s</option>""" % (i, i)
    return render_template("lectures.html", deneme=deneme1, deneme2="""""")


@app.route("/schedule")
def schedule():
    return render_template("schedule.html")


@app.route("/users")
def people_page():
    db = current_app.config["db"]
    people = db.get_people()
    return render_template("people.html", people=sorted(people))


@app.route("/users/<int:person_key>")
def person_page(person_key):
    db = current_app.config["db"]
    person = db.get_person(person_key)
    if person is None:
        abort(404)
    return render_template("person.html", person=person)


@app.route('/lectures', methods=['POST'])
def lectureregistry():
    names = ["physics", "biology", "chemistry"]
    deneme1 = """"""
    for i in names:
        deneme1 += """<option value="%s">%s</option>""" % (i, i)
    if request.method == "POST":
        car_brand = request.form.get("cars", None)
    return render_template("lectures.html", deneme=deneme1, deneme2=car_brand)


@app.route('/', methods=['POST'])
def my_form_post():
    if request.form["btn"] == "Sign Up":
        username = request.form['UserName']
        password = pbkdf2_sha256.hash(request.form['Password'])
        firstname = request.form['FirstName']
        lastname = request.form['LastName']
        statement = """INSERT INTO Persons (UserName, Password, FirstName, LastName) 
        VALUES ('%s', '%s', '%s', '%s');""" % (username, password, firstname, lastname)
        with psycopg2.connect(
                """dbname='lsgowduy' user='lsgowduy' host='salt.db.elephantsql.com' 
                password='FbiQok5ytKXzEjdU7MbH46l5AWJbKf3I'""") as connection:
            with connection.cursor() as cursor:
                cursor.execute(statement)
        flash('Signed Up successfully.')
        return render_template("homepage.html")
    elif request.form["btn"] == "Sign In":
        username = request.form['UserName']
        password = request.form['Password']
        statement = """SELECT password from Persons WHERE username = '%s'""" % (username,)
        with psycopg2.connect(
                """dbname='lsgowduy' user='lsgowduy' host='salt.db.elephantsql.com' 
                password='FbiQok5ytKXzEjdU7MbH46l5AWJbKf3I'""") as connection:
            with connection.cursor() as cursor:
                cursor.execute(statement)
                password1 = cursor.fetchone()[0]
                if pbkdf2_sha256.verify(password, password1):
                    return render_template("loggedin.html")
                else:
                    return """False information!Please try again"""

    return """nothing"""


if __name__ == "__main__":
    app.run()
