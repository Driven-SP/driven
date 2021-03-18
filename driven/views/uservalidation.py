#  from collections import namedtuple
#  from datetime import date
#  from flask import render_template
#  from flask import request
#  from flask import escape
from driven.db import get_db, execute

#  give a connection to datebasae and other credential info this will register a new user
#  todo: it is important to note that it will not do any sort validation as of now
def registerNewUser(conn, username, email_address, password):
    return execute(conn, "INSERT INTO UserValidation (username, email_address, password) VALUES (:username, :email_address, :password)", {'username': username, 'email_address': email_address, 'password': password})

#  todo: this is a very insecure validation system here
def validateUser(conn, username, password):
    user_info = execute(conn, "SELECT :username from UserValidation", { "username": username} )

    # todo: verify that this gets the correct information from database
    username_db = user_info[0].values()[0]
    password_db = user_info[0].values()[1]

    if username_db == username and password_db == password:
        return True

    return False

#  todo: implement this after session logic
def loginUser(username, password):
    with get_db() as conn:
        if validateUser(conn, username, password):
            # this is a very bad way to maintain the logged in username
            pass

#  todo: implement this after session logic
def logoutUser():
    pass
