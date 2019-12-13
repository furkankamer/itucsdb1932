import os
import sys

import psycopg2 as dbapi2

INIT_STATEMENTS = [
    """CREATE TABLE if not exists Users ( id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL );""",
	
	"""CREATE TABLE if not exists Building ( id SERIAL PRIMARY KEY, 
	name varchar(255) NOT NULL, 
	size int NOT NULL);""",
	
	"""CREATE TABLE if not exists Lectures ( id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    crn DEC(3,0) NOT NULL UNIQUE,
    time VARCHAR(255),
    weekday VARCHAR(255),
    locationid int NOT NULL,
	FOREIGN KEY (locationid)REFERENCES Building(id),
    quota DEC(3,0));""",
	
    """CREATE TABLE if not exists Teachers ( id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    profile bytea,
    join_date DATE NOT NULL DEFAULT CURRENT_DATE,
	lecture_id int NOT NULL,
	FOREIGN KEY (lecture_id) REFERENCES Lectures(id),
	experience_year Dec(2,0),
    user_id int NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id));""",

    """CREATE TABLE if not exists Managers ( id SERIAL PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    profile bytea,
    join_date DATE NOT NULL DEFAULT CURRENT_DATE,
	experience_year Dec(2,0),
    user_id int NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id));""",

    """CREATE TABLE if not exists Students ( id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    degree int NOT NULL,
    join_date DATE NOT NULL DEFAULT CURRENT_DATE,
    grade FLOAT,
	lecture_id int NOT NULL,
	FOREIGN KEY (lecture_id) REFERENCES Lectures(id),
    user_id int NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id));""",

    """CREATE TABLE if not exists Etudes ( id SERIAL PRIMARY KEY,
    subject VARCHAR(255),
    lecture_id int, 
	FOREIGN KEY (lecture_id) REFERENCES Lectures(id),
    time DATE NOT NULL,
    day VARCHAR(255),
    required_grade int,
    locationid int NOT NULL, 
	FOREIGN KEY (locationid) REFERENCES Building(id),
    quota DEC(3,0));""",
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
