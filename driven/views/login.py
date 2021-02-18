from flask import render_template

#  RenderFunctions
def views(bp):
    @bp.route("/login")
    def viewPLogin():
        return render_template("login.html")
