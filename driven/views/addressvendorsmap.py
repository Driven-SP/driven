from collections import namedtuple
from flask import render_template
from flask import request
from flask import escape
from driven.db import get_db, execute

#  HelperFunctions
def viewAddressVendorsMapHelper(conn):
    return execute(conn, "SELECT vendor_id, address_id, vendor_access FROM AddressVendorsMap")

def insertAddressVendorInDB(conn, vendor_id, address_id):
    print(vendor_id, address_id)
    vendor_access = 1
    # if vendor_id or not address:
    #     raise Exception
    return execute(
    conn,
    "INSERT INTO AddressVendorsMap (vendor_id, address_id, vendor_access) VALUES (:vendor_id, :address_id, :vendor_access);", {'vendor_id': vendor_id, 'address_id': address_id, 'vendor_access': vendor_access}
    )

def deleteVendorAddressAssociationFromDB(conn, vendor_id, address_id):
    if address_id in ("", None) and vendor_id in ("", None):
        raise Exception
    return execute(
    conn,
    "DELETE FROM AddressVendorsMap WHERE address_id = :address_id AND vendor_id = :vendor_id;", {'address_id': address_id, 'vendor_id': vendor_id}
    )

def revokeVendorAddressAssociationFromDB(conn, vendor_id, address_id):
    if address_id in ("", None) and vendor_id in ("", None):
        raise Exception
    return execute(
    conn,
    "UPDATE AddressVendorsMap SET vendor_access = 0 WHERE address_id = :address_id AND vendor_id = :vendor_id;", {'address_id': address_id, 'vendor_id': vendor_id}
    )

def grantVendorAddressAssociationFromDB(conn, vendor_id, address_id):
    if address_id in ("", None) and vendor_id in ("", None):
        raise Exception
    return execute(
    conn,
    "UPDATE AddressVendorsMap SET vendor_access = 1 WHERE address_id = :address_id AND vendor_id = :vendor_id;", {'address_id': address_id, 'vendor_id': vendor_id}
    )

#  RenderFunctions
def views(bp):
    @bp.route("/addressvendorsmap")
    def viewAddressVendorsMap():
        with get_db() as conn:
            rows = viewAddressVendorsMapHelper(conn)
        return render_template("table.html", name="AddressVendorsMap", rows=rows)

    @bp.route("/addressvendorsmap/add", methods = ['POST', 'GET'])
    def renderAddAddressVendorsMapForm():
        attributes = {"VendorId" : "number", "AddressId": "number" }
        return render_template("form.html", name="Add a Vendor for an Address: ", URI="/addressvendorsmap/add/submit",  submit_message="Add Vendor for the address", attributes=attributes)

    @bp.route("/addressvendorsmap/add/submit", methods = ['POST', 'GET'])
    def AddAddressVendorsMap():
        with get_db() as conn:
            vendor_id = request.form.get("VendorId")
            address_id = request.form.get("AddressId")
            try:
                insertAddressVendorInDB(conn, vendor_id, address_id)
            except Exception:
                return render_template("form_error.html", errors=["Your insertions did not went through check your inputs again."])
        return viewAddressVendorsMap()

    @bp.route("/addressvendorsmap/remove")
    def removeVendorAddressAssociation():
        with get_db() as conn:
            vendor_id = request.args.get("VendorId")
            address_id = request.args.get("AddressId")
            print("Vendor ID", vendor_id)
            try:
                deleteVendorAddressAssociationFromDB(conn, vendor_id, address_id)
            except Exception:
                return render_template("form_error.html", errors=["Your deletion did not went through check your inputs again."])
        return viewAddressVendorsMap()

    @bp.route("/addressvendorsmap/revoke_access")
    def revokeVendorAddressAssociation():
        with get_db() as conn:
            vendor_id = request.args.get("VendorId")
            address_id = request.args.get("AddressId")
            print("Vendor ID", vendor_id)
            try:
                revokeVendorAddressAssociationFromDB(conn, vendor_id, address_id)
            except Exception:
                return render_template("form_error.html", errors=["Your deletion did not went through check your inputs again."])
        return viewAddressVendorsMap()

    @bp.route("/addressvendorsmap/grant_access")
    def grantVendorAddressAssociation():
        with get_db() as conn:
            vendor_id = request.args.get("VendorId")
            address_id = request.args.get("AddressId")
            print("Vendor ID", vendor_id)
            try:
                grantVendorAddressAssociationFromDB(conn, vendor_id, address_id)
            except Exception:
                return render_template("form_error.html", errors=["Your deletion did not went through check your inputs again."])
        return viewAddressVendorsMap()
