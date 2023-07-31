#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Places """
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Retrieves all Place objects depending on the JSON in the body
       of the request
    """
    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()

    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    places = []
    if not states and not cities and not amenities:
        places = storage.all(Place).values()
    else:
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    if city:
                        places.extend(city.places)

        for city_id in cities:
            city = storage.get(City, city_id)
            if city and city not in places:
                places.extend(city.places)

        if amenities:
            places = [place for place in places
                      if all(am in place.amenities for am in amenities)]

    result = [place.to_dict() for place in places]
    return jsonify(result), 200
