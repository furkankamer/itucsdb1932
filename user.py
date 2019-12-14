from flask import current_app
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.active = True
        self.is_admin = False

    def get_id(self):
        return self.username

    @property
    def is_active(self):
        return self.active


def get_user(user_id):
    statement = """SELECT * FROM Users WHERE username = '%s'""" % (user_id,)
    with psycopg2.connect(url) as connection:
        with connection.cursor() as cursor:
            cursor.execute(statement)
            user = cursor.fetchone()
            return user
    # password = current_app.config["PASSWORDS"].get(user_id)
    # user = User(user_id, password) if password else None
    # if user is not None:
    #    user.is_admin = user.username in current_app.config["ADMIN_USERS"]
    # return user
