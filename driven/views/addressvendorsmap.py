from flask import render_template, request

# might not need all these methods
def viewAddressVendorsMapHelper(conn):
    pass

def deleteVendorAddressAssociationFromDB(conn, vendor_id, address_id):
    pass

def revokeVendorAddressAssociationFromDB(conn, vendor_id, address_id):
    pass

def grantVendorAddressAssociationFromDB(conn, vendor_id, address_id):
    pass

#  RenderFunctions
def views(bp):
    @bp.route("/addressvendorsmap")
    def viewAddressVendorsMap():
        pass

    @bp.route("/addressvendorsmap/add", methods = ['POST', 'GET'])
    def renderAddAddressVendorsMapForm():
        pass

    @bp.route("/addressvendorsmap/add/submit", methods = ['POST', 'GET'])
    def AddAddressVendorsMap():
        pass

    @bp.route("/addressvendorsmap/remove")
    def removeVendorAddressAssociation():
        pass

    @bp.route("/addressvendorsmap/revoke_access")
    def revokeVendorAddressAssociation():
        pass

    @bp.route("/addressvendorsmap/grant_access")
    def grantVendorAddressAssociation():
        pass
