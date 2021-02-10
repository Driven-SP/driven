from collections import namedtuple
from flask import render_template
from flask import request
from flask import escape
from driven.db import get_db, execute

#  HelperFunctions
def viewAddressHelper(conn):
    return execute(conn, "SELECT address_id, user_id, address, start_date, end_date FROM Address")

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
            rows = viewAddressHelper(conn)
        return render_template("table.html", name="Address", rows=rows)

    @bp.route("/address/add", methods = ['POST', 'GET'])
    def renderAddAddressForm():
        attributes = {"UserId" : "number", "Address": "text", "StartDate" : "text", "EndDate" : "text" }
        return render_template("form.html", name="Add Address: ", URI="/address/add/submit",  submit_message="Add Address", attributes=attributes)

    @bp.route("/address/add/submit", methods = ['POST', 'GET'])
    def addAddress():
        with get_db() as conn:
            user_id = request.form.get("UserId")
            address = request.form.get("Address")
            start_date = request.form.get("StartDate")
            end_date = request.form.get("EndDate")
            try:
                insertAddressInDB(conn, user_id, address, start_date, end_date)
            except Exception:
                return render_template("form_error.html", errors=["Your insertions did not went through check your inputs again."])
        return viewAddress()

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
