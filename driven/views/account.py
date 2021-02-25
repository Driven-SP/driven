#  This will handle the login and signup endpoints for different kinds of users
from flask import render_template

#  RenderFunctions
def views(bp):
    @bp.route("/login")
    def viewLogin():
        return render_template("login.html")

def views(bp):
    @bp.route("/signup")
    def viewSignup():
        #  todo: here redirect to home page if the user is already logged in cause it does not make
        #  sense for prompting logged in user to sign up
        return render_template("signup.html")
