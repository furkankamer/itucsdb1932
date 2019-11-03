from flask import Flask, render_template, request
import psycopg2




app = Flask(__name__)

def postgres_test():

	try:
		conn = psycopg2.connect(
			"dbname='lsgowduy' user='lsgowduy' host='salt.db.elephantsql.com' password='FbiQok5ytKXzEjdU7MbH46l5AWJbKf3I'")
		conn.close();
		return True
	except:
		print('not connected')
		return

if  postgres_test():
	print('connected')
	conn = psycopg2.connect(
			"dbname='lsgowduy' user='lsgowduy' host='salt.db.elephantsql.com' password='FbiQok5ytKXzEjdU7MbH46l5AWJbKf3I'")
	cursor = conn.cursor()
	statement = """CREATE TABLE if not exists Persons ( UserName varchar(255), Password varchar(255), FirstName varchar(255), LastName varchar(255) )"""
	cursor.execute(statement)
	conn.commit();
	conn.close();

    


@app.route("/")
def home_page():
    return render_template("homepage.html")


@app.route("/signup")
def sign_up():
	return render_template("signup.html")


@app.route('/', methods=['POST'])
def my_form_post():
	conn = psycopg2.connect(
			"dbname='lsgowduy' user='lsgowduy' host='salt.db.elephantsql.com' password='FbiQok5ytKXzEjdU7MbH46l5AWJbKf3I'")
	cursor = conn.cursor()
	username = request.form['UserName']
	password = request.form['Password']
	firstname = request.form['FirstName']
	lastname = request.form['LastName']
	statement = """INSERT INTO Persons (UserName, Password, FirstName, LastName)
VALUES ('%s', '%s', '%s', '%s');""" % (username,password,firstname,lastname)
	cursor.execute(statement)
	conn.commit();
	conn.close();
	return """Congratulations. You have signed up!"""





if __name__ == "__main__":
    app.run()