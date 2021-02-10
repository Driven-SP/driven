from collections import namedtuple
from flask import render_template
from flask import request
from flask import escape
from driven.db import get_db, execute
from flask import redirect

#  HelperFunctions
def viewUsersHelper(conn):
    return execute(conn, "SELECT user_id, fname, email, phone FROM Users")

def insertUserInDB(conn, fname, lname, email, phone):
    invalid = ("", None)
    if fname in invalid or lname in invalid or email in invalid:
        raise Exception
    return execute(
    conn,
    "INSERT INTO Users (fname, lname, email, phone) VALUES (:fname, :lname, :email, :phone);", {'fname': fname, 'lname': lname, 'email': email, 'phone': phone}
    )

def deleteUserFromDB(conn, user_id):
    if user_id in ("", None):
        raise Exception
    return execute(
    conn,
    "DELETE FROM Users WHERE user_id = :user_id;", {'user_id': user_id}
    )

def getAllAddressesForUserHelper(conn, user_id):
    if user_id in ("", None):
        raise Exception
    return execute(
    conn,
    "SELECT DISTINCT Users.user_id, Users.fname, Users.lname, Address.address_id, Address.address, Address.start_date, Address.end_date FROM (Address INNER JOIN Users ON Address.user_id = Users.user_id) WHERE Users.user_id = :user_id;", {'user_id': user_id}
    )

def changeAddressForAUserHelper(conn, address_id, address):
    if address_id in ("", None) or address_id in ("", None):
        raise Exception
    return execute(
    conn,
    "UPDATE Address SET address = :address WHERE address_id = :address_id;", {'address_id' : address_id, 'address' : address}
    )

#  RenderFunctions
def views(bp):
    @bp.route("/users")
    def viewUsers():
        with get_db() as conn:
            rows = viewUsersHelper(conn)
        return render_template("table.html", name="Users", rows=rows)

    @bp.route("/users/add", methods = ['POST', 'GET'])
    def renderAddUsersForm():
        attributes = {"FirstName" : "text", "LastName": "text", "Email" : "Text", "Phone" : "Text" }
        return render_template("form.html", name="Add Users: ", URI="/users/add/submit",  submit_message="Add User", attributes=attributes)

    @bp.route("/users/add/submit", methods = ['POST', 'GET'])
    def addUsers():
        with get_db() as conn:
            fname = request.form.get("FirstName")
            lname = request.form.get("LastName")
            email = request.form.get("Email")
            phone = request.form.get("Phone")
            try:
                insertUserInDB(conn, fname, lname, email, phone)
            except Exception:
                return render_template("form_error.html", errors=["Your insertions did not went through check your inputs again."])
        return viewUsers()

    @bp.route("/users/remove")
    def removeUser():
        with get_db() as conn:
            user_id = request.args.get("UserId")
            print("Here :",user_id)
            try:
                deleteUserFromDB(conn, user_id)
            except Exception:
                return render_template("form_error.html", errors=["Your deletion did not went through check your inputs again."])
        return viewUsers()

    @bp.route("/users/addresses")
    def getAllAddressesForUser():
        with get_db() as conn:
            user_id = request.args.get("UserId")
            try:
                rows = getAllAddressesForUserHelper(conn, user_id)
            except Exception:
                return render_template("form_error.html", errors=["Your request did not went through check your inputs again."])
        return render_template("table.html", name="Addresses for the User : " + user_id, rows=rows)

    @bp.route("/users/address/change")
    def changeAddressForAUser():
        with get_db() as conn:
            address_id = request.args.get("AddressId")
            address = request.args.get("address")
            print("Here ", address_id, address)
            try:
                rows = changeAddressForAUserHelper(conn, address_id, address)
            except Exception:
                return render_template("form_error.html", errors=["Your request did not went through check your inputs again."])
        return redirect('/address')
