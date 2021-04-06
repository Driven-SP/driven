'''
Sample cURL request:
curl -X POST -H 'Content-Type: application/json' -d '{"driven_mail_username":"anmol", "driven_mail_user_password":"anmol-password","driven_mail_vendor_id":"amazon", "driven_mail_vendor_token":"afdasfafa"}' http://localhost:5000/api/getAddress
'''

from flask import jsonify, request
from driven.firestore_api import getUserAddressesVendor, getDocumentIdOfUser, validateCredUser


#  RenderFunctions
def views(bp):
    @bp.route("/api/getAddress", methods=["POST"])
    def viewGetAddress():
        data = request.get_json()
        username = data["driven_mail_username"]
        user_password = data["driven_mail_user_password"]
        vendor_id = data["driven_mail_vendor_id"]
        vendor_token = data["driven_mail_vendor_token"]

        user_doc_id = getDocumentIdOfUser(username)
        user_valid = validateCredUser(user_doc_id, user_password)
        if user_valid is False:
            address_id_to_address = ""
        else:
            address_id_to_address = getUserAddressesVendor(
                vendor_id, vendor_token, user_doc_id)

        #  we get None when the vendor fails to validate with its vendor_id and token
        if address_id_to_address is None:
            address_id_to_address = ""

        message = {
            'status': 200,
            'message': 'OK',
            'address_id_to_address': address_id_to_address
        }
        resp = jsonify(message)
        resp.status_code = 200
        return resp
