from flask import render_template

def views(bp):
    @bp.route("/")
    def index():
        #  todo: this endpoint is often used for redirection, so check user login status
        #  if logged in show the user's homepage, otherwise show regular homepage for logged out user
        return render_template("index.html")
