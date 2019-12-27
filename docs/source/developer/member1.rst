Parts Implemented by Muhammed Furkan Kamer
==========================================

Database Design
---------------

I implemented three tables and two extra tables in this project: *Users*, *Lectures* and *Etudes* and *registeredstudents*,*building*.

In my tables;

.. figure:: ../img/ferdiagram.png
    :width: 100 %
    :alt: map to buried treasure

    E/R diagram for managers, teachers and students.

Code
----

The implementation of tables in the database is done using the following code block:

.. code-block:: python
    :name: dbinit.py

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
	
Sign Up Function
^^^^^^^^^^^^^^^^^^	

Code
----

Sign-Up function implemented as a function when form is posted from html page.
It first gets posted data from the form and if it is not in error, it inserts new user
to Users table. Then it also inserts other tables (Students, Teachers, Managers) according to
given title information.

.. code-block:: python
    :name: server.py
	
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


Lectures Function
^^^^^^^^^^^^^^^^^^	

Code
----

Lecture function can be seen as 2 parts. These parts are according to title of the user:

1. If user is Teacher, html select tags prepared to use in lectures.html template. After the 
select tags prepared, it checks if a form is being post. If a form is post, it takes selected
values from select tags in the form and it checks if the lecture informations are overlaps with
any other lecture and if it overlaps a error message is sent to render_template. If no error occurs
it runs SQL query to insert new lecture to the table.

2. If user is student, it first implements html list for open lectures using a select sql statement to
get existing lectures and then it adds them to the template. After this task completed it checks again a 
form post. If form posted it detects which row of lecture selected using checked radio button. Then it gets
id of lecture to use registry. Then it checks if student have another lecture that overlaps with new lecture,
if it is then an error message is send to render_template. If no error occurs then it inserts lecture id to *registeredstudents*
table and user id also to use it in other processes. The function is then completed.

.. code-block:: python
    :name: server.py
	
    @login_required
    @app.route("/lectures", methods=['GET', 'POST'])
    def lectures():
        if not current_user.is_authenticated:
            return redirect("/")
        title = """"""
        statement = """select title from users where username = '%s'""" % (current_user.username,)
        with psycopg2.connect(url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(statement)
                title = cursor.fetchone()[0]
        if title == "Teacher":
            error = """"""
            names = ["Physics", "Biology", "Chemistry"]
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            times = ["9:30", "11:30", "13:30", "15:30"]
            locations = ["MED A34", "EHB 2101", "MDB A105"]
            quotas = ['1', '30', '45', '60']
            branches = """"""
            day = """"""
            time = """"""
            location = """"""
            quota = """"""
            for i in names:
                branches += """<option value="%s">%s</option>""" % (i, i)
            for i in days:
                day += """<option value="%s">%s</option>""" % (i, i)
            for i in times:
                time += """<option value="%s">%s</option>""" % (i, i)
            for i in locations:
                location += """<option value="%s">%s</option>""" % (i, i)
            for i in quotas:
                quota += """<option value="%s">%s</option>""" % (i, i)
            if request.method == "POST":
                branch = request.form.get("Branch", None)
                weekday = request.form.get("day", None)
                lecturetime = request.form.get("time", None)
                lecturelocation = request.form.get("location", None)
                lecturequota = request.form.get("quota", None)
                statement = """
                INSERT INTO Lectures (name, time, weekday, location_id, quota,teacher_id,enrolled) 
                VALUES('%s','%s','%s',(SELECT id from Buildings where name = '%s'),'%s',(select id from Teachers where user_id = (select id from users where username = '%s')),0)""" % (
                    branch, lecturetime, weekday, lecturelocation, lecturequota, current_user.username)
                with psycopg2.connect(url) as connection:
                    with connection.cursor() as cursor:
                        try:
                            cursor.execute(statement)
                        except psycopg2.DatabaseError:
                            error = """You have already have a lecture at the same time. Please check your schedule"""
            return render_template("lectures.html", branchnames=branches, day=day, time=time, location=location,
                               quota=quota, title=title, message=error)
        else:
            error = """"""
            if request.method == "POST":
                k = 0
                err = 0
                for i in range(11, 30000, 10):
                    id = """%d""" % (i)
                    subject = request.form.get(id, None)
                    if subject is not None:
                        k = i - 1
                        break
                print(k)
                if k == 0:
                    return redirect("/lectures")
                id = """%d""" % (k)
                lidd = request.form.get(id, None)
                if lidd is not None:
                    statement1 = """insert into registeredstudents (lecture_id,student_id) values( %s, (select id from users where username = '%s')); update lectures set enrolled = enrolled + 1 where id = %s """ % (
                    lidd, current_user.username, lidd)
                    statement2 = """select lecture_id from registeredstudents where lecture_id is not null and student_id = (select id from users where username = '%s')""" % (
                        current_user.username)
                    statement4 = """select weekday,time from lectures where id = %s""" % (lidd)
                    with psycopg2.connect(url) as connection:
                        with connection.cursor() as cursor:
                            cursor.execute(statement2)
                            reglec = cursor.fetchall()
                            cursor.execute(statement4)
                            lecc = cursor.fetchall()
                            lweekd = lecc[0][0]
                            ltimee = lecc[0][1]
                            if reglec is not None:
                                for row in reglec:
                                    statement3 = """select weekday,time from lectures where id = %s""" % (row[0])
                                    cursor.execute(statement3)
                                    wreglec = cursor.fetchall()
                                    for lrow in wreglec:
                                        if lrow[0] == lweekd and lrow[1] == ltimee:
                                            error = """You have already have a lecture at the same time. Please check your schedule"""
                                            err = 1
                            if (err == 0):
                                cursor.execute(statement1)

            statement = """select id,name,weekday, time, quota from lectures"""
            lecturerows = """"""
            with psycopg2.connect(url) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(statement)
                    i = 10
                    for rows in cursor.fetchall():
                        lid = rows[0]
                        branch = rows[1]
                        weekday = rows[2]
                        lecturetime = rows[3]
                        lecturequota = rows[4]
                        lecturerows += """<tr><td>%s<input type="hidden" name="%d" value = "%s"/></td><td>%s</td><td>%s</td><td>%s</td> <td>%s</td>
                          <td><input id="%d" onclick="uncheck(%d)" type="radio" name="%d" value="%d"></td></tr>""" % (
                        lid, i, lid,
                        branch, weekday, lecturetime, lecturequota, i + 1, i + 1, i + 1, i + 1)
                        i += 10
            return render_template("lectures.html", title=title, newrow=lecturerows, message=error)

Etudes Function
^^^^^^^^^^^^^^^^^^	

Code
----

Etudes function can be seen as 2 parts. These parts are according to title of the user:

1. If user is Teacher, html select tags prepared to use in etudes.html template. After the 
select tags prepared, it checks if a form is being post. If a form is post, it takes selected
values from select tags in the form and it checks if the etude informations are overlaps with
any other etude and if it overlaps a error message is sent to render_template. If no error occurs
it runs SQL query to insert new etude to the table.

2. If user is student, it first implements html list for open etudes using a select sql statement to
get existing etudes and then it adds them to the template. After this task completed it checks again a 
form post. If form posted it detects which row of etude selected using checked radio button. Then it gets
id of etude to use registry. Then it checks if student have another etude that overlaps with new etude,
if it is then an error message is send to render_template. If no error occurs then it inserts etude id to *registeredstudents*
table and user id also to use it in other processes. The function is then completed.

.. code-block:: python
    :name: server.py

    @login_required
    @app.route("/etudes", methods=['GET', 'POST'])
    def etudes():
        if not current_user.is_authenticated:
            return redirect("/")
        title = """"""
        statement = """select title from users where username = '%s'""" % (current_user.username,)
        with psycopg2.connect(url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(statement)
                title = cursor.fetchone()[0]
        if title == "Teacher":
            with psycopg2.connect(url) as connection:
                with connection.cursor() as cursor:
                    statement = """select subject from Teachers where user_id = (select id from users where username = '%s')""" % (
                        current_user.username)
                    cursor.execute(statement)
                    subject = cursor.fetchone()[0]
            error = """"""
            if subject == "Physics":
                names = ["Electrics", "Acceleration", "Magnetism"]
            elif subject == "Biology":
                names = ["Bacteria", "Cell Division", "DNA"]
            elif subject == "Chemistry":
                names = ["Compounds", "Organics", "Acids"]
            days = ["Friday", "Saturday"]
            times = ["9:30", "11:30", "13:30", "15:30", "16:30", "17:30"]
            locations = ["MED A34", "EHB 2101", "MDB A105"]
            quotas = ['1', '30', '45', '60']
            branches = """"""
            day = """"""
            time = """"""
            location = """"""
            quota = """"""
            for i in names:
                branches += """<option value="%s">%s</option>""" % (i, i)
            for i in days:
                day += """<option value="%s">%s</option>""" % (i, i)
            for i in times:
                time += """<option id = "%s" value="%s">%s</option>""" % (i, i, i)
            for i in locations:
                location += """<option value="%s">%s</option>""" % (i, i)
            for i in quotas:
                quota += """<option value="%s">%s</option>""" % (i, i)
            if request.method == "POST":
                branch = request.form.get("Branch", None)
                weekday = request.form.get("day", None)
                lecturetime = request.form.get("time", None)
                lecturelocation = request.form.get("location", None)
                lecturequota = request.form.get("quota", None)
                statement = """
                INSERT INTO Etudes (subject, time, weekday, location_id, quota,teacher_id,enrolled) 
                VALUES('%s','%s','%s',(SELECT id from Buildings where name = '%s'),'%s',(select id from Teachers where user_id = (select id from users where username = '%s')),0)""" % (
                    branch, lecturetime, weekday, lecturelocation, lecturequota, current_user.username)
                with psycopg2.connect(url) as connection:
                    with connection.cursor() as cursor:
                        try:
                            cursor.execute(statement)
                        except psycopg2.DatabaseError:
                            error = """You have already have a lecture at the same time. Please check your schedule"""
            return render_template("etudes.html", branchnames=branches, day=day, time=time, location=location,
                                   quota=quota, title=title, message=error)
        else:
            error = """"""
            if request.method == "POST":
                k = 0
                err = 0
                for i in range(11, 30000, 10):
                    id = """%d""" % (i)
                    subject = request.form.get(id, None)
                    if subject is not None:
                        k = i - 1
                        break
                print(k)
                if k == 0:
                    return redirect("/etudes")
                id = """%d""" % (k)
                lidd = request.form.get(id, None)
                statement1 = """insert into registeredstudents (etude_id,student_id) values( %s, (select id from users where username = '%s')); update etudes set enrolled = enrolled+1 where id = %s """ % (
                lidd, current_user.username, lidd)
                statement2 = """select etude_id from registeredstudents where student_id = (select id from users where username = '%s') and etude_id is not null""" % (
                    current_user.username)
                statement4 = """select weekday,time from etudes where id = %s""" % (lidd)
                with psycopg2.connect(url) as connection:
                    with connection.cursor() as cursor:
                        cursor.execute(statement2)
                        reglec = cursor.fetchall()
                        cursor.execute(statement4)
                        lecc = cursor.fetchall()
                        lweekd = lecc[0][0]
                        ltimee = lecc[0][1]
                        print(reglec)
                        if reglec is not None:
                            for row in reglec:
                                statement3 = """select weekday,time from etudes where id = %s""" % (row[0])
                                cursor.execute(statement3)
                                wreglec = cursor.fetchall()
                                for lrow in wreglec:
                                    if lrow[0] == lweekd and lrow[1] == ltimee:
                                        error = """You have already have a etude at the same time. Please check your schedule"""
                                        err = 1
                        if (err == 0):
                            cursor.execute(statement1)

            statement = """select id,subject,weekday, time, quota from etudes"""
            lecturerows = """"""
            with psycopg2.connect(url) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(statement)
                    i = 10
                    for rows in cursor.fetchall():
                        lid = rows[0]
                        branch = rows[1]
                        weekday = rows[2]
                        lecturetime = rows[3]
                       lecturequota = rows[4]
                        lecturerows += """<tr><td>%s<input type="hidden" name="%d" value = "%s"/></td><td>%s</td><td>%s</td><td>%s</td> <td>%s</td>
                          <td><input id="%d" onclick="uncheck(%d)" type="radio" name="%d" value="%d"></td></tr>""" % (
                        lid, i, lid,
                        branch, weekday, lecturetime, lecturequota, i + 1, i + 1, i + 1, i + 1)
                        i += 10
            return render_template("etudes.html", title=title, newrow=lecturerows, message=error)








	