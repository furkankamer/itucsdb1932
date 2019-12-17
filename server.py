from flask import Flask, render_template, request, flash, current_app, abort, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import psycopg2
from passlib.hash import pbkdf2_sha256
from user import get_user
from database import Database

app = Flask(__name__)

app.secret_key = b'\xdd\xd6]j\xb0\xcc\xe3mNF{\x14\xaf\xa7\xb9\x17'

lm = LoginManager()

db = Database()

url = "dbname='lsgowduy' user='lsgowduy' host='salt.db.elephantsql.com' password='FbiQok5ytKXzEjdU7MbH46l5AWJbKf3I'"


@lm.user_loader
def load_user(user_id):
    return get_user(user_id)


@app.route("/login", methods=['POST'])
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
    if not current_user.is_authenticated:
        return redirect("/")
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


@login_required
@app.route("/profile")
def profile():
    if not current_user.is_authenticated:
        return redirect("/")
    titles = """select title from users where username = '%s'""" % (current_user.username,)
    with psycopg2.connect(url) as connection:
        with connection.cursor() as cursor:
            cursor.execute(titles)
            title = cursor.fetchone()[0]
            if title == "Manager":
                statement = """SELECT * FROM Managers WHERE user_id = (SELECT id FROM Users WHERE username = '%s')""" \
                            % (current_user.username,)
                cursor.execute(statement)
                for row in cursor.fetchall():
                    print(row)
                    name = row[1]
                    surname = row[2]
                    email = row[3]
                    join_date = row[4]
                    experience = row[5]
                return render_template("profile.html",
                                       username=current_user.username, title=title, name=name, surname=surname,
                                       email=email, join_date=join_date, experience=experience)
            elif title == "Teacher":
                statement = """SELECT * FROM Teachers WHERE user_id = (SELECT id FROM Users WHERE username = '%s')""" \
                            % (current_user.username,)
                cursor.execute(statement)
                for row in cursor.fetchall():
                    print(row)
                    name = row[1]
                    surname = row[2]
                    subject = row[3]
                    join_date = row[4]
                    experience = row[5]
                return render_template("profile.html",
                                       username=current_user.username, title=title, name=name, surname=surname,
                                       subject=subject, join_date=join_date, experience=experience)
            elif title == "Student":
                statement = """SELECT * FROM Students WHERE user_id = (SELECT id FROM Users WHERE username = '%s')""" \
                            % (current_user.username,)
                cursor.execute(statement)
                for row in cursor.fetchall():
                    print(row)
                    name = row[1]
                    surname = row[2]
                    degree = row[3]
                    join_date = row[4]
                    grade = row[5]
                return render_template("profile.html",
                                       username=current_user.username, title=title, name=name, surname=surname,
                                       degree=degree, join_date=join_date, grade=grade)
            else:
                abort(404)


@login_required
@app.route("/update-profile")
def profile_update():
    if not current_user.is_authenticated:
        return redirect("/")
    query = """SELECT id, title FROM Users WHERE username = '%s'""" % (current_user.username,)
    with psycopg2.connect(url) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            for row in cursor.fetchall():
                print(row)
                user_id = row[0]
                title = row[1]
            if title == "Manager":
                query = """SELECT name, surname, email, experience_year FROM Managers WHERE user_id = %s""" % (user_id,)
                cursor.execute(query)
                for row in cursor.fetchall():
                    name = row[0]
                    surname = row[1]
                    email = row[2]
                    experience = row[3]
                return render_template("update-profile.html", name=name, surname=surname, email=email,
                                       experience=experience)
            elif title == "Teacher":
                query = """SELECT name, surname, subject, experience_year FROM Teachers WHERE user_id = %s""" % user_id
                cursor.execute(query)
                for row in cursor.fetchall():
                    name = row[0]
                    surname = row[1]
                    subject = row[2]
                    experience = row[3]
                return render_template("update-profile.html",
                                       name=name, surname=surname, subject=subject, experience=experience)
            elif title == "Student":
                query = """SELECT name, surname, degree FROM Students WHERE user_id = %s""" % (user_id,)
                cursor.execute(query)
                for row in cursor.fetchall():
                    name = row[0]
                    surname = row[1]
                    degree = row[2]
                return render_template("update-profile.html", name=name, surname=surname, degree=degree)
            else:
                abort(404)


@login_required
@app.route("/update-profile", methods=['POST'])
def update_profile():
    if not current_user.is_authenticated:
        return redirect("/")
    query = """SELECT id, title FROM Users WHERE username = '%s'""" % (current_user.username,)
    with psycopg2.connect(url) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            for row in cursor.fetchall():
                print(row)
                user_id = row[0]
                title = row[1]
            if title == "Manager":
                name = request.form['name']
                surname = request.form['surname']
                email = request.form['email']
                experience = request.form['experience']
                query = """UPDATE Managers SET name = '%s', surname = '%s', email = '%s', experience_year = %s 
                WHERE user_id = %s""" % (name, surname, email, experience, user_id)
                cursor.execute(query)
                query = """UPDATE Users SET name = '%s', surname = '%s' WHERE id = %s""" % (name, surname, user_id)
                cursor.execute(query)
                connection.commit()
            elif title == "Teacher":
                name = request.form['name']
                surname = request.form['surname']
                subject = request.form['subject']
                experience = request.form['experience']
                query = """UPDATE Teachers SET name = '%s', surname = '%s', subject = '%s', experience_year = %s 
                WHERE user_id = %s""" % (name, surname, subject, experience, user_id)
                cursor.execute(query)
                query = """UPDATE Users SET name = '%s', surname = '%s' WHERE id = %s""" % (name, surname, user_id)
                cursor.execute(query)
                connection.commit()
            elif title == "Student":
                name = request.form['name']
                surname = request.form['surname']
                degree = request.form['degree']
                query = """UPDATE Students SET name = '%s', surname = '%s', degree = %s WHERE user_id = %s""" % (
                    name, surname, degree, user_id)
                cursor.execute(query)
                query = """UPDATE Users SET name = '%s', surname = '%s' WHERE id = %s""" % (name, surname, user_id)
                cursor.execute(query)
                connection.commit()
    return redirect("/profile")


@login_required
@app.route("/password")
def password():
    if not current_user.is_authenticated:
        return redirect("/")
    return render_template("password.html")


@login_required
@app.route("/password", methods=['POST'])
def change_password():
    if not current_user.is_authenticated:
        return redirect("/")
    new1 = request.form['new1']
    new2 = request.form['new2']
    if new1 != new2:
        message = "New passwords don't match. Try again."
        return render_template("password.html", message=message)
    old = request.form['old']
    user = get_user(current_user.username)
    if pbkdf2_sha256.verify(old, user.password):
        new = pbkdf2_sha256.hash(new1)
        query = """UPDATE Users SET password = '%s' WHERE username = '%s'""" % (new, current_user.username)
        with psycopg2.connect(url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                logout_user()
                return redirect("/signin")
    else:
        message = "The old password you entered is incorrect. Try again."
        return render_template("password.html", message=message)


@login_required
@app.route("/DELETE")
def delete():
    if not current_user.is_authenticated:
        return redirect("/")
    query = """SELECT id, title FROM Users WHERE username = '%s'""" % (current_user.username,)
    with psycopg2.connect(url) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            for row in cursor.fetchall():
                user_id = row[0]
                title = row[1]
            title += "s"
            query = """DELETE FROM %s WHERE user_id = %s""" % (title, user_id)
            try:
                cursor.execute(query)
            except psycopg2.DatabaseError:
                if title == "Teachers":
                    message = "A teacher should quit from his/her lectures/etudes before deleting its account."
                    return render_template("homepage.html", message=message)
                else:
                    abort(404)
            logout_user()
            if title == "Students":
                query = """DELETE FROM RegisteredStudents WHERE student_id = %s""" % user_id
                cursor.execute(query)
            query = """DELETE FROM Users WHERE id = %s""" % user_id
            cursor.execute(query)
            connection.commit()
            return redirect("/")


@login_required
@app.route("/students")
def students():
    if not current_user.is_authenticated:
        return redirect("/")
    query = """SELECT title FROM Users WHERE username = '%s'""" % (current_user.username,)
    with psycopg2.connect(url) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            title = cursor.fetchone()[0]
            if title != "Student":
                query = """SELECT * from Students ORDER BY id"""
                cursor.execute(query)
                rows = []
                for row in cursor.fetchall():
                    print(row)
                    rows += (row,)
                print(rows)
                return render_template("students.html", students=rows)
            else:
                return redirect("/")


@login_required
@app.route("/student", methods=['POST'])
def give_grade():
    if not current_user.is_authenticated:
        return redirect("/")
    student_id = request.form['id']
    query = """SELECT name, surname, degree, join_date, grade FROM Students WHERE id = %s""" % (student_id,)
    with psycopg2.connect(url) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            for row in cursor.fetchall():
                if row[0] is None:
                    return redirect("/students")
                elif row[0] == "":
                    return redirect("/students")
                name = row[0]
                surname = row[1]
                degree = row[2]
                join_date = row[3]
                grade = row[4]
                return render_template("student.html", id=student_id, name=name, surname=surname, degree=degree,
                                       join_date=join_date, grade=grade)
            return redirect("/students")


@login_required
@app.route("/teachers")
def teachers():
    if not current_user.is_authenticated:
        return redirect("/")
    query = """SELECT title FROM Users WHERE username = '%s'""" % (current_user.username,)
    with psycopg2.connect(url) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            title = cursor.fetchone()[0]
            if title == "Manager":
                query = """SELECT * from Teachers ORDER BY id"""
                cursor.execute(query)
                rows = []
                for row in cursor.fetchall():
                    print(row)
                    rows += (row,)
                print(rows)
                return render_template("teachers.html", teachers=rows)
            else:
                return redirect("/")


@login_required
@app.route("/grade", methods=['POST'])
def grader():
    if not current_user.is_authenticated:
        return redirect("/")
    query = """UPDATE Students SET grade = %s WHERE id = %s""" % (request.form['grade'], request.form['id'])
    with psycopg2.connect(url) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
            return redirect("/students")


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


@login_required
@app.route("/schedule", methods=['GET', 'POST'])
def schedule():
    if not current_user.is_authenticated:
        return redirect("/")
    statement = """SELECT title FROM Users WHERE username = '%s'""" % (current_user.username,)
    schedulerows = """<tr>"""
    with psycopg2.connect(url) as connection:
        with connection.cursor() as cursor:
            cursor.execute(statement)
            title = cursor.fetchone()[0]
            if title == "Manager":
                message = "Managers don't have a schedule."
                return render_template("homepage.html", message=message)
            others = title
            others += "s"
            if title == "Teacher":
                if request.method == "POST":
                    if request.form['sub'] == "Delete":
                        lecidd = request.form.get("LecID", None)
                        etdidd = request.form.get("EtudeID", None)
                        if lecidd is not None and lecidd != "":
                            statement = """delete from registeredstudents where lecture_id = %s""" % (lecidd)
                            cursor.execute(statement)
                            statement = """delete from lectures where id = %s""" % (lecidd)
                            cursor.execute(statement)
                        elif etdidd is not None and etdidd != "":
                            statement = """delete from registeredstudents where etude_id = %s""" % (etdidd)
                            cursor.execute(statement)
                            statement = """delete from etudes where id = %s""" % (etdidd)
                            cursor.execute(statement)
                    elif request.form['sub'] == "Update":
                        lecidd = request.form.get("LecID2", None)
                        etdidd = request.form.get("EtudeID2", None)
                        if lecidd is not None and lecidd != "":
                            statement = """update lectures set weekday = '%s', time = '%s', quota = %s, location_id = (select id from buildings where name = '%s') 
                                       where id = %s and teacher_id = (select id from teachers where user_id = (select id from users where username = '%s'))""" % (
                            request.form['wday'], request.form['timee'],
                            request.form['lquotaa'], request.form['lcation'], lecidd, current_user.username)
                            cursor.execute(statement)
                        elif etdidd is not None and etdidd != "":
                            statement = """update etudes set weekday = '%s', time = '%s', quota = %s, location_id = (select id from buildings where name = '%s') 
                                       where id = %s and teacher_id = (select id from teachers where user_id = (select id from users where username = '%s'))""" % (
                            request.form['etudewday'], request.form['timee2'],
                            request.form['lquotaa'], request.form['lcation'], etdidd, current_user.username)
                            print(statement)
                            cursor.execute(statement)
                statement = """SELECT id,name, time, weekday, location_id, quota FROM Lectures WHERE teacher_id = (
            SELECT id FROM %s WHERE user_id = (SELECT id FROM Users WHERE username = '%s')) order by time""" \
                            % (others, current_user.username)
                cursor.execute(statement)
                lname = ""
                lcrn = 0
                ltime = '00:00'
                lweekday = ""
                llocation_id = 0
                lquota = 0
                schedule1 = cursor.fetchall()
                statement = """SELECT id,subject, time, weekday, location_id, quota FROM Etudes WHERE teacher_id = (
            SELECT id FROM %s WHERE user_id = (SELECT id FROM Users WHERE username = '%s')) order by time""" \
                            % (others, current_user.username)
                cursor.execute(statement)
                etdschedule = cursor.fetchall()
                if schedule1 is not None:
                    Monday = """<th>"""
                    Tuesday = """<th>"""
                    Wednesday = """<th>"""
                    Thursday = """<th>"""
                    Friday = """<th>"""
                    Saturday = """<th>"""
                    for row in schedule1:
                        print(row)
                        lname = row[1]
                        lcrn = row[0]
                        ltime = row[2]
                        lweekday = row[3]
                        llocation_id = row[4]
                        lquota = row[5]
                        statement = """SELECT name FROM Buildings WHERE id = %s""" % (llocation_id,)
                        cursor.execute(statement)
                        llocation = ""
                        for row in cursor.fetchall():
                            print(row)
                            llocation = row[0]
                        if lweekday == "Monday":
                            Monday += """<p>Lecture ID: %s</p><p>%s</p><p>%s</p><p>%s</p><p>Quota: %s</p>""" % (
                            lcrn, lname, ltime, llocation, lquota)
                        elif lweekday == "Tuesday":
                            Tuesday += """<p>Lecture ID: %s</p><p>%s</p><p>%s</p><p>%s</p><p>Quota: %s</p>""" % (
                            lcrn, lname, ltime, llocation, lquota)
                        elif lweekday == "Wednesday":
                            Wednesday += """<p>Lecture ID: %s</p><p>%s</p><p>%s</p><p>%s</p><p>Quota: %s</p>""" % (
                            lcrn, lname, ltime, llocation, lquota)
                        elif lweekday == "Thursday":
                            Thursday += """<p>Lecture ID: %s</p><p>%s</p><p>%s</p><p>%s</p><p>Quota: %s</p>""" % (
                            lcrn, lname, ltime, llocation, lquota)
                        elif lweekday == "Friday":
                            Friday += """<p>Lecture ID: %s</p><p>%s</p><p>%s</p><p>%s</p><p>Quota: %s</p>""" % (
                            lcrn, lname, ltime, llocation, lquota)
                    if etdschedule is not None:
                        for row in etdschedule:
                            lname = row[1]
                            lcrn = row[0]
                            ltime = row[2]
                            lweekday = row[3]
                            llocation_id = row[4]
                            lquota = row[5]
                            statement = """SELECT name FROM Buildings WHERE id = %s""" % (llocation_id,)
                            cursor.execute(statement)
                            llocation = ""
                            for row in cursor.fetchall():
                                print(row)
                                llocation = row[0]
                            if lweekday == "Friday":
                                Friday += """<p>Etude ID: %s</p><p>%s</p><p>%s</p><p>%s</p><p>Quota: %s</p>""" % (
                                lcrn, lname, ltime, llocation, lquota)
                            elif lweekday == "Saturday":
                                Saturday += """<p>Etude ID: %s</p><p>%s</p><p>%s</p><p>%s</p><p>Quota: %s</p>""" % (
                                lcrn, lname, ltime, llocation, lquota)
                    Monday += """</th>"""
                    Tuesday += """</th>"""
                    Wednesday += """</th>"""
                    Thursday += """</th>"""
                    Friday += """</th>"""
                    Saturday += """</th>"""
                    schedulerows += Monday + Tuesday + Wednesday + Thursday + Friday + Saturday
                    schedulerows += """</tr>"""
                    return render_template("schedule.html", newrow=schedulerows, title=title)
            elif title == "Student":
                statement = """select lecture_id from registeredstudents where student_id = (select id from users where username ='%s') and lecture_id is not null""" \
                            % (current_user.username)

                Monday = """<th>"""
                Tuesday = """<th>"""
                Wednesday = """<th>"""
                Thursday = """<th>"""
                Friday = """<th>"""
                Saturday = """<th>"""
                with psycopg2.connect(url) as connection:
                    with connection.cursor() as cursor:
                        if request.method == "POST":
                            lecidd = request.form.get("LecID", None)
                            etdidd = request.form.get("EtudeID", None)
                            if lecidd is not None and lecidd != "":
                                statement1 = """delete from registeredstudents where lecture_id = %s and student_id = (select id from users where username = '%s'); update
                                 lectures set enrolled = enrolled - 1 where id = %s""" % (
                                lecidd, current_user.username, lecidd)
                                cursor.execute(statement1)
                            elif etdidd is not None and etdidd != "":
                                statement1 = """delete from registeredstudents where etude_id = %s and student_id = (select id from users where username = '%s'); update
                                 etudes set enrolled = enrolled - 1 where id = %s""" % (
                                etdidd, current_user.username, etdidd)
                                cursor.execute(statement1)
                        cursor.execute(statement)
                        lids = cursor.fetchall()
                        if lids is not None:
                            for lirow in lids:
                                lid = lirow[0]
                                if lid is not None:
                                    statement = """SELECT id,name, time, weekday, location_id, quota FROM Lectures where id = %s""" % (
                                        lid)
                                    cursor.execute(statement)
                                    lname = ""
                                    lcrn = 0
                                    ltime = '00:00'
                                    lweekday = ""
                                    llocation_id = 0
                                    lquota = 0
                                    schedule1 = cursor.fetchall()
                                    if schedule1 is not None:
                                        for row in schedule1:
                                            print(row)
                                            lname = row[1]
                                            lcrn = row[0]
                                            ltime = row[2]
                                            lweekday = row[3]
                                            llocation_id = row[4]
                                            lquota = row[5]
                                            statement = """SELECT name FROM Buildings WHERE id = %s""" % (llocation_id,)
                                            cursor.execute(statement)
                                            llocation = ""
                                            for lorow in cursor.fetchall():
                                                print(lorow)
                                                llocation = lorow[0]
                                            if lweekday == "Monday":
                                                Monday += """<p>Lecture ID: %s</p><p>%s</p><p>%s</p><p>%s</p><p>Quota: %s</p>""" % (
                                                lcrn, lname, ltime, llocation, lquota)
                                            elif lweekday == "Tuesday":
                                                Tuesday += """<p>Lecture ID: %s</p><p>%s</p><p>%s</p><p>%s</p><p>Quota: %s</p>""" % (
                                                lcrn, lname, ltime, llocation, lquota)
                                            elif lweekday == "Wednesday":
                                                Wednesday += """<p>Lecture ID: %s</p><p>%s</p><p>%s</p><p>%s</p><p>Quota: %s</p>""" % (
                                                lcrn, lname, ltime, llocation, lquota)
                                            elif lweekday == "Thursday":
                                                Thursday += """<p>Lecture ID: %s</p><p>%s</p><p>%s</p><p>%s</p><p>Quota: %s</p>""" % (
                                                lcrn, lname, ltime, llocation, lquota)
                                            elif lweekday == "Friday":
                                                Friday += """<p>Lecture ID: %s</p><p>%s</p><p>%s</p><p>%s</p><p>Quota: %s</p>""" % (
                                                lcrn, lname, ltime, llocation, lquota)
                        statement = """select etude_id from registeredstudents where student_id = (select id from users where username ='%s') and etude_id is not null""" \
                                    % (current_user.username)
                        cursor.execute(statement)
                        etdlids = cursor.fetchall()
                        if etdlids is not None:
                            for etdrow in etdlids:
                                etdlid = etdrow[0]
                                if etdlid is not None:
                                    statement = """SELECT id,subject, time, weekday, location_id, quota FROM etudes where id = %s""" % (
                                        etdlid)
                                    cursor.execute(statement)
                                    etdschedule = cursor.fetchall()
                                    lname = ""
                                    lcrn = 0
                                    ltime = '00:00'
                                    lweekday = ""
                                    llocation_id = 0
                                    lquota = 0
                                    if etdschedule is not None:
                                        for row in etdschedule:
                                            lname = row[1]
                                            lcrn = row[0]
                                            ltime = row[2]
                                            lweekday = row[3]
                                            llocation_id = row[4]
                                            lquota = row[5]
                                            statement = """SELECT name FROM Buildings WHERE id = %s""" % (llocation_id,)
                                            cursor.execute(statement)
                                            llocation = ""
                                            for row in cursor.fetchall():
                                                print(row)
                                                llocation = row[0]
                                            if lweekday == "Friday":
                                                Friday += """<p>Etude ID: %s</p><p>%s</p><p>%s</p><p>%s</p><p>Quota: %s</p>""" % (
                                                lcrn, lname, ltime, llocation, lquota)
                                            elif lweekday == "Saturday":
                                                Saturday += """<p>Etude ID: %s</p><p>%s</p><p>%s</p><p>%s</p><p>Quota: %s</p>""" % (
                                                lcrn, lname, ltime, llocation, lquota)
                                    Monday += """</th>"""
                                    Tuesday += """</th>"""
                                    Wednesday += """</th>"""
                                    Thursday += """</th>"""
                                    Friday += """</th>"""
                                    Saturday += """</th>"""
                                    schedulerows += Monday + Tuesday + Wednesday + Thursday + Friday + Saturday
                                    print(schedulerows)
                                    schedulerows += """</tr>"""
                return render_template("schedule.html", newrow=schedulerows)


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


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return redirect("/")


lm.init_app(app)
lm.login_view = "login"

app.config["db"] = db

if __name__ == "__main__":
    app.run()
