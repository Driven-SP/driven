'''
Sample cURL requests:
curl -X POST -H 'Content-Type: application/json' -d '{"driven_mail_username":"anmol", "driven_mail_user_password":"anmol-password","driven_mail_vendor_id":"amazon", "driven_mail_vendor_token":"afdasfafa"}' http://localhost:5000/api/getAddress

curl -X POST -H 'Content-Type: application/json' -d '{"driven_mail_username":"anmol", "driven_mail_vendor_id":"amazon","tracking_num":"randomtrackingnumber", "status":"RECORD CREATED", "status_description":"Package record created at 11:00pm"}' http://localhost:5000/api/createPackageRecord

curl -X POST -H 'Content-Type: application/json' -d '{"driven_mail_username":"anmol", "package_id":"kfArsEseMmcPyDXpJmk2", "status":"IN PROGRESS", "status_description":"Received at local facility"}' http://localhost:5000/api/updatePackageRecord

curl -X POST -H 'Content-Type: application/json' -d '{"driven_mail_username":"anmol", "package_id":"kfArsEseMmcPyDXpJmk2", "status":"DELIVERED", "status_description":"Received at local facility"}' http://localhost:5000/api/updatePackageRecord
'''

from flask import jsonify, request
from driven.firestore_api import getUserAddressesVendor, getDocumentIdOfUser, validateCredUser, createPackageRecord, updatePackageStatus


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

    @bp.route("/api/createPackageRecord", methods=["POST"])
    def viewsCreatePackageRecord():
        data = request.get_json()
        username = data["driven_mail_username"]
        vendor_id = data["driven_mail_vendor_id"]
        tracking_num = data["tracking_num"]
        status = data["status"]
        status_description = data["status_description"]

        package_doc_id = createPackageRecord(tracking_num, status, status_description, vendor_id, username)

        message = {
            'status': 200,
            'message': 'OK',
            'package_id': package_doc_id
        }
        resp = jsonify(message)
        resp.status_code = 200
        return resp

    @bp.route("/api/updatePackageRecord", methods=["POST"])
    def viewUpdatePackageRecord():
        data = request.get_json()
        username = data["driven_mail_username"]
        package_doc_id = data["package_id"]
        status = data["status"]
        status_description = data["status_description"]

        package_record_updated = updatePackageStatus(username, package_doc_id, status, status_description)

        operation_result = "Package record failed to update"
        if package_record_updated:
            operation_result = "Package record updated"

        message = {
            'status': 200,
            'message': 'OK',
            'operation_result': operation_result
        }
        resp = jsonify(message)
        resp.status_code = 200
        return resp
