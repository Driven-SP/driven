from flask import Blueprint
from driven.views import index
from driven.views import users
from driven.views import address
from driven.views import vendors
from driven.views import profile
from driven.views import addressvendorsmap

blueprint = Blueprint('views', __name__)
index.views(blueprint)
users.views(blueprint)
address.views(blueprint)
vendors.views(blueprint)
profile.views(blueprint)
addressvendorsmap.views(blueprint)

def init_app(app):
    app.register_blueprint(blueprint)
    app.add_url_rule('/', endpoint='index')
