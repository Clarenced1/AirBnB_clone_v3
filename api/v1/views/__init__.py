#!/usr/bin/python3
"""This module define a blueprint for routes with Blueprint object"""
from flask import Blueprint

<<<<<<< HEAD

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

=======
>>>>>>> d3250fe63a49cc068fbf97090565dce97a0e1b56
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
<<<<<<< HEAD
from api.v1.views.places_amenities import *
=======
from api.v1.views.states import *
from api.v1.views.users import *


app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
>>>>>>> d3250fe63a49cc068fbf97090565dce97a0e1b56
