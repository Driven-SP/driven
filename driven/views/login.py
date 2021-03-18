from flask import render_template

#  RenderFunctions
def views(bp):
    @bp.route("/login")
    def viewLogin():
        return render_template("login.html")
