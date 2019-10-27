from flask import Flask, render_template
import os
import urllib.parse as up
import psycopg2

def postgres_test():

    try:
        conn = psycopg2.connect("dbname='lsgowduy' user='lsgowduy' host='salt.db.elephantsql.com' password='FbiQok5ytKXzEjdU7MbH46l5AWJbKf3I'")
        conn.close()
        return True
    except:
        return 
		

if  postgres_test():
	conn = psycopg2.connect("dbname='lsgowduy' user='lsgowduy' host='salt.db.elephantsql.com' password='FbiQok5ytKXzEjdU7MbH46l5AWJbKf3I'")
	cursor=conn.cursor()
	app = Flask(__name__)
	statement ="""CREATE TABLE if not exists Persons (
    UserName varchar(255),
    Password varchar(255),
    FirstName varchar(255),
    LastName varchar(255)
);"""
	cursor.execute(statement)

@app.route("/")
def home_page():
    return render_template("homepage.html")


if __name__ == "__main__":
    app.run()
