from flask import render_template, request, session, redirect
from  driven.firestore_api import getIdAddressMap, getPrimaryAddress, addAddressUser

def views(bp):
    @bp.route("/address", methods= ['GET'])
    def viewAddress():
        try:
            curr_username = session["username"]
            curr_user_doc_id = session["user_document_id"]
            user_primary_address = getPrimaryAddress(curr_user_doc_id)
            user_active_id_and_addresses = getIdAddressMap(curr_user_doc_id, "ACTIVE")
            user_inactive_id_and_addresses = getIdAddressMap(curr_user_doc_id, "INACTIVE")

            return render_template("profile.html", name=curr_username, primary_address=user_primary_address, active_id_and_addresses=user_active_id_and_addresses, inactive_id_and_addresses=user_inactive_id_and_addresses)

        except:
            return redirect("/login")
 
    @bp.route("/address/remove")
    def removeAddress():
        pass

    @bp.route("/address/revive")
    def reviveAddress():
        pass

    @bp.route("/address/changePrimary")
    def changePrimaryAddress():
        pass

    @bp.route("/add_address", methods= ['POST', 'GET'])
    def addAddress():
        user_document_id = ""
        #  validate user is logged in
        try:
            user_document_id = session["user_document_id"]
        except:
            return redirect("/login")

        if request.method == 'GET':
            return render_template("add_address.html")

        elif request.method == 'POST':
            #  todo: also add some sort of form validation so that user given input is in correct
            #  format, right now it accepts any string
            street = request.form.get("Street").strip()
            city = request.form.get("City").strip()
            state = request.form.get("State").strip()
            zip_id = request.form.get("Zip").strip()
            full_address = '{}, {}, {} {}'.format(street, city, state, zip_id)

            try:
                addAddressUser(user_document_id, full_address)
            except Exception:
                return render_template("form_error.html", errors=["Failed to add new address"])

            #  if successful insertion, show the user's current address
            return redirect("/profile")
