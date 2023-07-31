#!/usr/bin/python3
"""This module implement a rule that return a view"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity
from flasgger.utils import swag_from


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
@swag_from('documentation/place/get_places.yml', methods=['GET'])
def place_by_city(city_id):
    """View function that return place objects by city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
@swag_from('documentation/place/get_place.yml', methods=['GET'])
def show_place(place_id):
    """Endpoint that return a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
@swag_from('documentation/place/delete_place.yml', methods=['DELETE'])
def delete_place(place_id):
    """Endpoint that delete a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
@swag_from('documentation/place/post_place.yml', methods=['POST'])
def insert_place(city_id):
    """Endpoint that insert a Place object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    res = request.get_json()
    if not isinstance(res, dict):
        abort(400, description="Not a JSON")
    if not res.get("user_id"):
        abort(400, description="Missing user_id")
    user = storage.get(User, res.get("user_id"))
    if user is None:
        abort(404)
    if not res.get("name"):
        abort(400, description="Missing name")
    new_place = Place(**res)
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@swag_from('documentation/place/post_search.yml', methods=['POST'])
def update_place(place_id):
    """Endpoint that update a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    res = request.get_json()
    if not isinstance(res, dict):
        abort(400, description="Not a JSON")
    for key, value in res.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending of the JSON in the body
    of the request
    """

    if request.get_json() is None:
        abort(400, description="Not a JSON")

    data = request.get_json()

    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)

    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)

    list_places = []
    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]

    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    return jsonify(places)
