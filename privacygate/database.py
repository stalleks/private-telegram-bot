import sqlite3
from datetime import datetime

from aiogram.types import User


connection = sqlite3.connect('db.sql')
cursor = connection.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS users ('
               'id integer NOT NULL PRIMARY KEY,'
               'username varchar(50),'
               'full_name varchar(50),'
               'url varchar(50),'
               'registration_date datetime,'
               'admin bool NOT NULL)'
               )
connection.commit()


def get_user(user_id: int):
    cursor.execute("SELECT * FROM users WHERE id = '%s'" % user_id)
    user = cursor.fetchall()
    return user[0] if len(user) > 0 else ()


def add_user(user: User):
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO users (id, username, full_name, url, registration_date, admin) "
                   "VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" %
                   (user.id, user.username, user.full_name, user.url, date_time, 0))
    connection.commit()


def add_user_by_attr(user_id: int, username: str, full_name: str, url: str):
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO users (id, username, full_name, url, registration_date, admin) "
                   "VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" %
                   (user_id, username, full_name, url, date_time, 0))
    connection.commit()

def update_user(id: int, filed: str, value: str):
    cursor.execute("UPDATE users SET '%s' = '%s' WHERE id = '%s'" % (filed, value, id))
    connection.commit()


def delete_user(user_id: int):
    cursor.execute("DELETE FROM users WHERE id = '%s'" % user_id)
    connection.commit()


def all_users():
    cursor.execute("SELECT * FROM users ORDER BY username")
    users = cursor.fetchall()
    return users


cursor.execute('CREATE TABLE IF NOT EXISTS subscription_requests ('
               'id integer NOT NULL PRIMARY KEY,'
               'username varchar(50),'
               'full_name varchar(50),'
               'url varchar(50),'
               'date_time datetime)'
               )
connection.commit()


def get_subscription_request(user_id: int):
    cursor.execute("SELECT * FROM subscription_requests WHERE id = '%s'" % user_id)
    request = cursor.fetchall()
    return request[0] if len(request) > 0 else ()


def add_subscription_request(user: User):
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO subscription_requests (id, username, full_name, url, date_time) "
                   "VALUES ('%s', '%s', '%s', '%s', '%s')" %
                   (user.id, user.username, user.full_name, user.url, date_time))
    connection.commit()


def update_subscription_request(id: int, filed: str, value: str):
    cursor.execute("UPDATE subscription_requests SET '%s' = '%s' WHERE id = '%s'" % (filed, value, id))
    connection.commit()


def delete_subscription_request(user_id: int):
    cursor.execute("DELETE FROM subscription_requests WHERE id = '%s'" % user_id)
    connection.commit()


def all_subscription_request():
    cursor.execute("SELECT * FROM subscription_requests ORDER BY username")
    users = cursor.fetchall()
    return users
