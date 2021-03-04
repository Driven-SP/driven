from flask import render_template

def views(bp):
    @bp.route("/")
    def index():
        #  todo: this endpoint is often used for redirection, so check user login status
        #  if logged in show the user's homepage, otherwise show regular homepage for logged out user

        #  todo: when a user is logged out, he/she will be redirected to this endpoint, so handle that
        #  logic here as well
        return render_template("index.html")
