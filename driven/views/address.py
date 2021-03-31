from collections import namedtuple
from datetime import date
from flask import render_template, request, escape, session, redirect
from driven.db import get_db, execute
from driven.firestore_api import addAddressUser

#  HelperFunctions
def viewAddressHelper(conn, user_id):
    return execute(conn, "SELECT address_id, :user_id, address, start_date, end_date FROM Address", {'user_id': user_id} )

def insertAddressInDB(conn, user_id, address, start_date, end_date):
    print(user_id, address, start_date, end_date)
    invalid = ("", None)
    if not user_id or address in invalid or user_id in invalid:
        raise Exception
    return execute(
    conn,
    "INSERT INTO Address (user_id, address, start_date, end_date) VALUES (:user_id, :address, :start_date, :end_date);", {'user_id': user_id, 'address': address, 'start_date': start_date, 'end_date': end_date}
    )

def deleteAddressFromDB(conn, address_id):
    if address_id in ("", None):
        raise Exception
    return execute(
    conn,
    "DELETE FROM Address WHERE address_id = :address_id;", {'address_id': address_id}
    )

def getAllVendprsForAddressHelper(conn, address_id):
    if address_id in ("", None):
        raise Exception
    return execute(
    conn,
    "SELECT AddressVendorsMap.address_id, Address.address, AddressVendorsMap.vendor_id, Vendors.vendor_name , AddressVendorsMap.vendor_access FROM ((AddressVendorsMap INNER JOIN Vendors ON AddressVendorsMap.vendor_id = Vendors.vendor_id) INNER JOIN Address ON AddressVendorsMap.address_id = Address.address_id) WHERE AddressVendorsMap.address_id = :address_id;", {'address_id': address_id}
    )
    
#  RenderFunctions
def views(bp):
    @bp.route("/address")
    def viewAddress():
        with get_db() as conn:
            #  todo: userid is hardcoded for 1 right now, need to change later, this is just for demo
            user_id = 1
            rows = viewAddressHelper(conn, user_id)
        return render_template("user-address.html", name="Address", rows=rows)

    @bp.route("/address/add", methods = ['POST', 'GET'])
    def renderAddAddressForm():
        #  todo: for startdate we can use the current date, for userid we need to get the current user from login context
        
        attributes = {"UserId" : "number", "Address": "text", "StartDate" : "text", "EndDate" : "text" }
        return render_template("form.html", name="Add Address: ", URI="/address/add/submit",  submit_message="Add Address", attributes=attributes)

    @bp.route("/address/remove")
    def removeAddress():
        with get_db() as conn:
            address_id = request.args.get("AddressId")
            print("Address ID", address_id)
            try:
                deleteAddressFromDB(conn, address_id)
            except Exception:
                return render_template("form_error.html", errors=["Your deletion did not went through check your inputs again."])
        return viewAddress()

    @bp.route("/address/vendors")
    def getAllVendprsForAddress():
        with get_db() as conn:
            address_id = request.args.get("AddressId")
            try:
                rows = getAllVendprsForAddressHelper(conn, address_id)
            except Exception:
                return render_template("form_error.html", errors=["Your request did not went through check your inputs again."])
        return render_template("table.html", name="Vendors for the Address : " + address_id, rows=rows)

    #  get request handles form for new address input by user
    #  post request handles submission of that form
    @bp.route("/add_address", methods= ['POST', 'GET'])
    def addAddress():
        user_document_id = ""
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
