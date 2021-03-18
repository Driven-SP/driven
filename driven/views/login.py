from flask import render_template
from flask import request

#  from driven.views import userValidation

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
            #  if loginUser(username, password) == True:
                #  return render_template("loginsuccessful.html")
            pass

