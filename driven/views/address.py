from flask import render_template, request, session, redirect
from  driven.firestore_api import getIdAddressMap, getPrimaryAddress, addAddressUser, deleteAddressUser, reviveAddressUser, changePrimaryAddressUser

def views(bp):
    @bp.route("/address", methods= ['GET', 'POST'])
    def viewAddress():
        try:
            curr_username = session["username"]
            curr_user_doc_id = session["user_document_id"]
            user_primary_address = getPrimaryAddress(curr_user_doc_id)
            user_active_id_and_addresses = getIdAddressMap(curr_user_doc_id, "ACTIVE")
            user_inactive_id_and_addresses = getIdAddressMap(curr_user_doc_id, "INACTIVE")

            return render_template("address.html", name=curr_username, primary_address=user_primary_address, active_id_and_addresses=user_active_id_and_addresses, inactive_id_and_addresses=user_inactive_id_and_addresses)

        except:
            return redirect("/login")
 
    @bp.route("/removeAddress", methods=['POST'])
    def removeAddress():
        try:
            user_document_id = session["user_document_id"]
            address_id = request.form.get("address_id")
            deleteAddressUser(user_document_id, address_id)
            return redirect("/address")
        except:
            #  todo: maybe redirect to login page cause it is possible that the user is not logged in
            return redirect("/address")

    @bp.route("/reviveAddress", methods=['POST'])
    def reviveAddress():
        try:
            user_document_id = session["user_document_id"]
            address_id = request.form.get("revive_address_id")
            reviveAddressUser(user_document_id, address_id)
            return redirect("/address")
        except:
            #  todo: maybe redirect to login page cause it is possible that the user is not logged in
            return redirect("/address")

    @bp.route("/changePrimaryAddress", methods=['POST'])
    def changePrimaryAddress():
        try:
            user_document_id = session["user_document_id"]
            address_id = request.form.get("address_id")
            changePrimaryAddressUser(user_document_id, address_id)
            return redirect("/address")
        except:
            #  todo: maybe redirect to login page cause it is possible that the user is not logged in
            return redirect("/address")

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
            return redirect("/address")

