import psycopg2 as dbapi2

url = "dbname='lsgowduy' user='lsgowduy' host='salt.db.elephantsql.com' password='FbiQok5ytKXzEjdU7MbH46l5AWJbKf3I'"


class Database:
    def __init__(self):
        self.dbfile = url

    def get_user(self, username):
        user = object()
        user.username = username
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """SELECT username, password, title, name, surname FROM Users WHERE username = %s""" % (username,)
            cursor.execute(query)
            curs = cursor.fetchall()
            user.password = curs[1]
            user.title = curs[2]
            user.name = curs[3]
            user.surname = curs[4]
        return user

    def update_user(self, user_id, user):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """UPDATE Users 
            SET " username = '%s', password = '%s' title = '%s' name = '%s' surname = '%s' WHERE (id = %s)""" % (
                user.username, user.password, user.title, user.name, user.surname, user_id)
            cursor.execute(query)
            connection.commit()

    def update_profile(self, user_id, profile):  # Changeable attributes: name, surname (general updating)
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT title FROM Users WHERE id = %s" % (user_id,)
            cursor.execute(query)
            title = cursor.fetchone()[0]
            title += "s"
            query = "UPDATE %s SET name = '%s', YR = %s WHERE (ID = %s)" % (
                title, profile.name, profile.surname, profile.id)
            cursor.execute(query)
            connection.commit()

    def delete_user(self, user_id, profile_id):  # Deletes user and profile
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT title FROM Users WHERE id = %s" % (user_id,)
            cursor.execute(query)
            title = cursor.fetchone()[0]
            title += "s"
            query = """DELETE FROM %s WHERE (id = %s)""" % (title, profile_id)
            cursor.execute(query)
            query = """DELETE FROM Users WHERE (id = %s)""" % (user_id,)
            cursor.execute(query)
            connection.commit()
