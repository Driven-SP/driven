from flask import Blueprint
from driven.views import index
from driven.views import address
from driven.views import profile
from driven.views import pricing
from driven.views import contact
from driven.views import login
from driven.views import addressvendorsmap

blueprint = Blueprint('views', __name__)
index.views(blueprint)
address.views(blueprint)
profile.views(blueprint)
pricing.views(blueprint)
contact.views(blueprint)
login.views(blueprint)
addressvendorsmap.views(blueprint)

def init_app(app):
    app.register_blueprint(blueprint)
    app.add_url_rule('/', endpoint='index')
