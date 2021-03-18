from flask import render_template

from  driven.views import address
from driven.db import get_db, execute

#  RenderFunctions
def views(bp):
    @bp.route("/profile")
    def viewProfile():
        with get_db() as conn:
            # todo: userid is hardcoded for 1 right now, need to change later, this is just for demo
            user_id = 1
            rows = address.viewAddressHelper(conn, user_id)
        return render_template("profile.html", name="Address", rows=rows)

