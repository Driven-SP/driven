#  todo : here, use flask-login for session management after the initial version works 

from driven.db import get_db, execute

#  todo: sync this with our local database later to store all the usenames that are currently active
ALL_LOGGED_IN_USERS = set()

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

#  todo: implement this cleanly after good session logic
def loginUser(username, password):
    with get_db() as conn:
        if validateUser(conn, username, password):
            # this is a very bad way to maintain the logged in username
            ALL_LOGGED_IN_USERS.add(username)
            return True

    return False

#  todo: implement this cleanly after good session logic
def logoutUser(username):
    #  todo: note that this does not ensure user will be removed from the list if they exit without
    #  clicking the logout button
    ALL_LOGGED_IN_USERS.remove(username)
