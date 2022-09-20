#!/usr/bin/python3
"""new view for Places objects that handles
all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/cities/<string:city_id>/places',
                 methods=['GET'], strict_slashes=False)
def places_get_from_city(city_id):
    """This method retrieve list of all places by city"""
    city = storage.get(City, city_id)
    if (city is None):
        abort(404)

    places = city.places
    if (places is None):
        abort(404)

    result = [obj.to_dict() for obj in places]

    return (jsonify(result))


@app_views.route('/places/<string:place_id>',
                 methods=['GET'], strict_slashes=False)
def places_get_id(place_id):
    """This method retrieve place by id"""
    place = storage.get(Place, place_id)
    if (place is None):
        abort(404)
    result = place.to_dict()
    return (jsonify(result))


@app_views.route('/places/<string:place_id>',
                 methods=['DELETE'], strict_slashes=False)
def place_delete(place_id):
    """This method delete place by id"""
    place_delete = storage.get(Place, place_id)
    if place_delete is None:
        abort(404)
    else:
        place_delete.delete()
        storage.save()
    return (jsonify({}), 200)


@app_views.route('/cities/<string:city_id>/places',
                 methods=['POST'], strict_slashes=False)
def place_post(city_id):
    """This method add a new place in city by id"""
    if (not storage.get(City, city_id)):
        abort(404)

    new_data = request.get_json(silent=True)

    if (type(new_data) is dict):
        new_place = Place(**new_data)
        setattr(new_place, "city_id", city_id)

        user_id = new_place.to_dict().get('user_id', None)
        if (not user_id):
            return jsonify({'message': 'Missing user_id'}), 400
        if (not storage.get(User, user_id)):
            abort(404)

        if (not new_place.to_dict().get('name', None)):
            return jsonify({'message': 'Missing name'}), 400

        new_place.save()
        return (jsonify(new_place.to_dict()), 201)

    return (jsonify({'message': 'Not a JSON'}), 400)


@app_views.route('/places/<string:place_id>',
                 methods=['PUT'], strict_slashes=False)
def place_put(place_id):
    """This method update city by id"""
    find_place = storage.get(Place, place_id)
    if (find_place is None):
        abort(404)

    update_place = request.get_json(silent=True)
    if (type(update_place) is dict):
        update_place.pop('id', None)
        update_place.pop('created_at', None)
        update_place.pop('updated_at', None)

        for key, value in update_place.items():
            setattr(find_place, key, value)
        find_place.save()
        return (jsonify(find_place.to_dict()), 200)

    return (jsonify({'message': 'Not a JSON'}), 400)
