from flask import render_template, session
from driven.firestore_api import getPackagesForDashboard


#  this handles showing the status of packages
def views(bp):
    @bp.route("/")
    def index():
        try:
            username = session["username"]
            user_document_id = session["user_document_id"]

            delivered_info, undelivered_info = getPackagesForDashboard(
                user_document_id)
            return render_template("dashboard.html",
                                   delivered_info=delivered_info,
                                   undelivered_info=undelivered_info)
        except:
            return render_template("index.html")
