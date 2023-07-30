from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Avoid wildcard import and import the specific views
from api.v1.views.index import api_status
