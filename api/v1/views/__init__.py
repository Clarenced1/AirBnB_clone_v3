#!/usr/bin/python3
"""This module define a blueprint for routes with Blueprint object"""
from flask import Blueprint


app_views = Blueprint("app_views", __name__, url_prefix='/api/v1')

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
from api.v1.views.places_amenities import *
>>>>>>> 83918d98bab2266b6c32569ab05930cc72d15348
