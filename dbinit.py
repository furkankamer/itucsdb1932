import os
import sys

import psycopg2 as dbapi2

INIT_STATEMENTS = [
    """CREATE TABLE if not exists Users ( id SERIAL UNIQUE, 
	username varchar(255) NOT NULL UNIQUE, 
	password varchar(255) NOT NULL,
	title varchar(255) NOT NULL,
	firstname varchar(255) NOT NULL, 
    surname varchar(255) NOT NULL );""",
    
	"""CREATE TABLE if not exists Lectures ( id SERIAL UNIQUE, 
	name varchar(255), 
	crn DEC(3,0) NOT NULL UNIQUE, 
	time varchar(255), 
    weekday varchar(255), 
	location int FOREIGN KEY REFERENCES Building(id) , 
	quota DEC(3,0));""",
	
	"""CREATE TABLE if not exists Etudes   ( id SERIAL UNIQUE, 
	subject varchar(255),
	lectureid int FOREIGN KEY REFERENCES Lectures(id) , 
	time datetime(0) 
    day varchar(255), 
	required_grade int, 
	location varchar(255)FOREIGN KEY REFERENCES Buildings(id), 
	quota DEC(3,0));""",
	
	"""CREATE TABLE if not exists Teachers ( id SERIAL UNIQUE, 
	name varchar(255), 
	crn DEC(3,0) NOT NULL UNIQUE, 
	time varchar(255), 
    day varchar(255), 
	location varchar(255), 
	quota DEC(3,0));""",
	
	"""CREATE TABLE if not exists Managers ( id SERIAL UNIQUE, 
	name varchar(255), 
	crn DEC(3,0) NOT NULL UNIQUE, 
	time varchar(255), 
    day varchar(255), 
	location varchar(255), 
	quota DEC(3,0));""",
	
	"""CREATE TABLE if not exists Students ( id SERIAL UNIQUE, 
	name varchar(255) NOT NULL, 
	surname varchar(255) NOT NULL, 
	degree int NOT NULL, 
	joindate DATE NOT NULL DEFAULT CURRENT_DATE, 
	grade float,
	userid int NOT NULL,
	FOREIGN KEY (userid) REFERENCES Users(id));""",
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = "dbname='lsgowduy' user='lsgowduy' host='salt.db.elephantsql.com' password='FbiQok5ytKXzEjdU7MbH46l5AWJbKf3I'"
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
