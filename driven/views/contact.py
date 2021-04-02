from flask import render_template


#  RenderFunctions
def views(bp):
    @bp.route("/contact")
    def viewContact():
        return render_template("contact.html")
