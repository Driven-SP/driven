from flask import render_template


#  RenderFunctions
def views(bp):
    @bp.route("/pricing")
    def viewPricing():
        return render_template("pricing.html")
