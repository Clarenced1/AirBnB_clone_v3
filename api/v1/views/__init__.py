from api.v1.views.index import api_status  # Import first

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
