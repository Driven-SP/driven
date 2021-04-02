from flask import render_template, session


def views(bp):
    @bp.route("/")
    def index():
        try:
            username = session["username"]
            user_document_id = session["user_document_id"]
            #  todo: when logged in, this page will show all package information
            return render_template("dashboard.html", username=username)
        except:
            return render_template("index.html")
