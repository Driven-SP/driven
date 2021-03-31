from flask import render_template, session, redirect
from  driven.firestore_api import getIdAddressMap, getPrimaryAddress

from  driven.views import address
from driven.db import get_db, execute

#  RenderFunctions
def views(bp):
    @bp.route("/profile")
    def viewProfile():
        try:
            curr_username = session["username"]
            curr_user_doc_id = session["user_document_id"]
            user_primary_address = getPrimaryAddress(curr_user_doc_id)
            user_active_id_and_addresses = getIdAddressMap(curr_user_doc_id, "ACTIVE")
            user_inactive_id_and_addresses = getIdAddressMap(curr_user_doc_id, "INACTIVE")

            return render_template("profile.html", name=curr_username, primary_address=user_primary_address, active_id_and_addresses=user_active_id_and_addresses, inactive_id_and_addresses=user_inactive_id_and_addresses)

        except:
            return redirect("/login")
