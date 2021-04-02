from flask import render_template, session, redirect, request
from driven.firestore_api import getUserProfileInfo, changeUsernameUser, changeFnameUser, changeLnameUser, changeEmailUser, changePhoneUser


#  RenderFunctions
def views(bp):
    @bp.route("/profile")
    def viewProfile():
        try:
            curr_username = session["username"]
            curr_user_doc_id = session["user_document_id"]

            user_profile_info = getUserProfileInfo(curr_user_doc_id)
            fname = user_profile_info["fname"]
            lname = user_profile_info["lname"]
            username = user_profile_info["username"]
            email = user_profile_info["email"]
            phone = user_profile_info["phone"]
            primary_address = user_profile_info["primary_address"]

            return render_template("profile.html",
                                   fname=fname,
                                   lname=lname,
                                   username=username,
                                   email=email,
                                   phone=phone,
                                   primary_address=primary_address)

        except:
            return redirect("/login")

    @bp.route("/changeProfileInfo", methods=['POST'])
    def changeProfileInfo():
        try:
            curr_username = session["username"]
            curr_user_doc_id = session["user_document_id"]

            field = request.form.get("field")
            value = request.form.get("value")
            placeholder = request.form.get("placeholder")

            return render_template("change-profile-info.html",
                                   field=field,
                                   value=value,
                                   placeholder=placeholder)

        except:
            return redirect("/login")

    @bp.route("/changeUsername", methods=['POST'])
    def changeUsername():
        try:
            curr_username = session["username"]
            curr_user_doc_id = session["user_document_id"]

            new_username = request.form.get("username")
            changeUsernameUser(curr_user_doc_id, new_username)

            return redirect("/profile")

        except:
            return redirect("/login")

    @bp.route("/changeFirstName", methods=['POST'])
    def changeFirstName():
        try:
            curr_username = session["username"]
            curr_user_doc_id = session["user_document_id"]

            new_fname = request.form.get("fname")
            changeFnameUser(curr_user_doc_id, new_fname)

            return redirect("/profile")

        except:
            return redirect("/login")

    @bp.route("/changeLastName", methods=['POST'])
    def changeLastName():
        try:
            curr_username = session["username"]
            curr_user_doc_id = session["user_document_id"]

            new_lname = request.form.get("lname")
            changeLnameUser(curr_user_doc_id, new_lname)

            return redirect("/profile")

        except:
            return redirect("/login")

    @bp.route("/changeEmailAddress", methods=['POST'])
    def changeEmailAddress():
        try:
            curr_username = session["username"]
            curr_user_doc_id = session["user_document_id"]

            new_email = request.form.get("email")
            changeEmailUser(curr_user_doc_id, new_email)

            return redirect("/profile")

        except:
            return redirect("/login")

    @bp.route("/changePhoneNumber", methods=['POST'])
    def changePhoneNumber():
        try:
            curr_username = session["username"]
            curr_user_doc_id = session["user_document_id"]

            new_phone = request.form.get("phone")
            changePhoneUser(curr_user_doc_id, new_phone)

            return redirect("/profile")

        except:
            return redirect("/login")
