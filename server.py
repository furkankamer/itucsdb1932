from flask import Flask, render_template, request, flash
import psycopg2
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)

app.secret_key = b'\xdd\xd6]j\xb0\xcc\xe3mNF{\x14\xaf\xa7\xb9\x17';


@app.route("/")
def home_page():
    return render_template("homepage.html")


@app.route("/signup")
def sign_up():
    return render_template("signup.html")


@app.route("/signin")
def sign_in():
    return render_template("signin.html")


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
        statement = """SELECT password from Persons WHERE username = '%s'""" % (username)
        with psycopg2.connect(
                """dbname='lsgowduy' user='lsgowduy' host='salt.db.elephantsql.com' 
                password='FbiQok5ytKXzEjdU7MbH46l5AWJbKf3I'""") as connection:
            with connection.cursor() as cursor:
                cursor.execute(statement)
                password1 = cursor.fetchone()[0]
                if pbkdf2_sha256.verify(password, password1):
                    return """Congratulations. You have signed in"""
                else:
                    return """False information!Please try again"""

    return """nothin"""


if __name__ == "__main__":
    app.run()
