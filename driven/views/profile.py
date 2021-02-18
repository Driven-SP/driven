from flask import render_template

#  RenderFunctions
def views(bp):
    @bp.route("/profile")
    def viewProfile():
        return render_template("profile.html")

