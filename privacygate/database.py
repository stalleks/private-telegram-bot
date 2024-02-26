import sqlite3
from datetime import datetime

from aiogram.types import User

users = {1636374994: {"name": "alex4", "admin": True},
         1636374990: {"name": "alex0", "admin": False},
         1636374995: {"name": "alex5", "admin": False},
         1636374999: {"name": "alex9", "admin": False},
         1636374993: {"name": "alex3", "admin": False},
         1636374992: {"name": "alex2", "admin": False},
         1636374996: {"name": "alex6", "admin": False},
         }
subscription_requests = {}


connection = sqlite3.connect('db.sql')
cursor = connection.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS users ('
               'id integer NOT NULL PRIMARY KEY,'
               'username varchar(50),'
               'full_name varchar(50),'
               'url varchar(50),'
               'admin bool NOT NULL)'
               )
connection.commit()


def get_user(user_id: int):
    cursor.execute("SELECT * FROM users WHERE id = '%s'" % user_id)
    return cursor.fetchall()


def add_user(user: User):
    cursor.execute("INSERT INTO users (id, username, full_name, url, admin) "
                   "VALUES ('%s', '%s', '%s', '%s', '%s')" %
                   (user.id, user.username, user.full_name, user.url, False))
    connection.commit()


def delete_user(user_id: int):
    cursor.execute("DELETE FROM users WHERE id = '%s'" % user_id)
    connection.commit()


def all_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    print(users)


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
    return cursor.fetchall()


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
    cursor.execute("SELECT * FROM subscription_requests")
    users = cursor.fetchall()
    print(users)
