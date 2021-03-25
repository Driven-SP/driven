from flask import render_template
from flask import request, session
from driven.firestore_api import validateCredUser 

#  RenderFunctions
def views(bp):
    @bp.route("/login", methods = ['POST', 'GET'])
    def viewLogin():
        # give the login form to user
        if request.method == 'GET':
            return render_template("login.html")

        #  try to submit and validate the login information
        elif request.method == 'POST':
            username = request.form.get("username")
            password = request.form.get("password")

            if validateCredUser(username, password) is True:
                session["username"] = username
                return render_template("profile.html")

        return render_template("login.html")
