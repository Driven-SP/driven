from flask import render_template, redirect
from flask import request, session
from driven.firestore_api import validateCredUser, signUpUser

#  RenderFunctions
def views(bp):
    @bp.route("/login", methods = ['POST', 'GET'])
    def viewLogin():
        # do not make session permanent
        #  even with this, session persists until browser is completely shut down
        session.permanent = False

        # give the login form to user
        if request.method == 'GET':
            # todo:  do not give login form if user already logged in
            return render_template("login.html")

        #  try to submit and validate the login information
        elif request.method == 'POST':
            username = request.form.get("username")
            password = request.form.get("password")

            if validateCredUser(username, password) is True:
                session["username"] = username
                return render_template("profile.html", name=session["username"])

        return render_template("login.html")


    @bp.route("/logout", methods = ['GET'])
    def viewLogout():
        session.pop("username", None)
        return redirect("/login")

    @bp.route("/signup", methods = ['GET', 'POST'])
    def viewSignup():
        if request.method == 'GET':
            return render_template("signup.html")
        elif request.method == 'POST':
            username = request.form.get("username")
            fname = request.form.get("fname")
            lname = request.form.get("lname")
            email = request.form.get("email")
            phone = request.form.get("phone")
            password = request.form.get("password")
            reenter_password = request.form.get("reenter_password")

            if (password == reenter_password) and (signUpUser(fname, lname, email, phone, username, password) is True):
                #  todo: give feedback regarding why the signup process was not successful
                return render_template("login.html")
        return render_template("signup.html")
