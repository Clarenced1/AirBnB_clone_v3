#!/usr/bin/python3
"""
Defines a new view for Place objects that handles all default
 RESTFul API actions
"""
from flask import jsonify, request, abort
from models import storage
from api.v1.views import app_views


@app_views.route('/api/v1/places_search', methods=['POST'],
                 strict_slashes=False)
def search_places():
    """
    Searches for Place objects based on the JSON body of the request.
    """
    try:
        data = request.get_json()
    except FileNotFoundError:
        abort(400, "Not a JSON")

    if data is None or not data:
        places = storage.all('Place').values()
        return jsonify([place.to_dict() for place in places])

    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    if not isinstance(states, list) or not isinstance(cities, list) \
            or not isinstance(amenities, list):
        abort(400, "Invalid data format")

    places = []

    if states or cities:
        for state_id in states:
            state = storage.get('State', state_id)
            if state:
                places += [place for place in state.places]
        for city_id in cities:
            city = storage.get('City', city_id)
            if city:
                places += [place for place in city.places]

    if amenities:
        amenities_ids = set(amenities)
        places = [place for place in places if amenities_ids.issubset(
            {a.id for a in place.amenities})]

    return jsonify([place.to_dict() for place in places])
