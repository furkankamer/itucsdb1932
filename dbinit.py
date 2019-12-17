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

    """CREATE TABLE if not exists Buildings ( id SERIAL PRIMARY KEY, 
    name varchar(255) NOT NULL, 
    size int);""",

    """CREATE TABLE if not exists Teachers ( id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    subject varchar(255),
    join_date DATE NOT NULL DEFAULT CURRENT_DATE,
    experience_year int,
    user_id int NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id));""",

    """CREATE TABLE if not exists Managers ( id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    join_date DATE NOT NULL DEFAULT CURRENT_DATE,
    experience_year int,
    user_id int NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id));""",

    """CREATE TABLE if not exists Students ( id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    degree int NOT NULL,
    join_date DATE NOT NULL DEFAULT CURRENT_DATE,
    grade FLOAT,
    user_id int NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id));""",

    """CREATE TABLE if not exists Lectures ( id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    time TIME,
    weekday VARCHAR(255),
    enrolled int DEFAULT 0,
    location_id int,
    FOREIGN KEY (location_id)REFERENCES Buildings(id),
    teacher_id int,
    FOREIGN KEY (teacher_id) REFERENCES Teachers (id),
    quota int,CONSTRAINT time_cons UNIQUE(time,weekday,location_id),
    CONSTRAINT teacher_cons UNIQUE(time,weekday,teacher_id));""",

    """CREATE TABLE if not exists Etudes ( id SERIAL PRIMARY KEY,
    subject VARCHAR(255),
    teacher_id int, 
    FOREIGN KEY (teacher_id) REFERENCES Teachers(id),
    time TIME,
    weekday VARCHAR(255),
    enrolled int DEFAULT 0,
    location_id int NOT NULL, 
    FOREIGN KEY (location_id) REFERENCES Buildings(id),
    quota int);""",

    """CREATE TABLE if not exists RegisteredStudents (
    lecture_id int, 
    FOREIGN KEY (lecture_id) REFERENCES Lectures(id),
    student_id int , 
    FOREIGN KEY (student_id) REFERENCES Users(id),
    etude_id int , 
    FOREIGN KEY (etude_id) REFERENCES Etudes(id),
    CONSTRAINT reg_cons UNIQUE(student_id,lecture_id),
    CONSTRAINT regi_cons UNIQUE(student_id,etude_id));""",
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
