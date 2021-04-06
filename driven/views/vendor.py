from flask import render_template, request, session, redirect
from driven.firestore_api import generateTokenVendor


#  RenderFunctions
def views(bp):
    @bp.route("/vendorToken", methods=['POST', 'GET'])
    def viewVendorToken():
        #  if user is logged in, clear seesion and redirect to index page
        try:
            if session["username"]:
                session.clear()
                return render_template("vendor-token.html")
        except:
            #  here, we know user is not logged in
            if request.method == "GET":
                return render_template("vendor-token.html")
            elif request.method == "POST":
                vendor_id = request.form.get("vendor_id")
                vendor_name = request.form.get("vendor_name")
                token = generateTokenVendor(vendor_id, vendor_name)

                #  when returned token is empty string, the vendor_id is not unique
                if token == "":
                    return render_template("vendor-token.html")
                else:
                    return render_template("show-vendor-token.html",
                                           vendor_name=vendor_name,
                                           vendor_id=vendor_id,
                                           vendor_token=token)
