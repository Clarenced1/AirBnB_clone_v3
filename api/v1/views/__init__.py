from flask import Blueprint

# Create a Blueprint instance
v1 = Blueprint('v1', __name__, url_prefix='/api/v1')

# Import views here (example):
# from api.v1.views.some_view import SomeViewClass

# Register the views (example):
# v1.add_url_rule('/some_endpoint', view_func=SomeViewClass.as_view
# ('some_endpoint'))
