#!/usr/bin/python3
"""new view for Cities objects that handles
all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<string:state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def cities_get_from_state(state_id):
    """This method retrieve list of all cities by state"""
    state = storage.get(State, state_id)
    if (state is None):
        abort(404)

    cities = state.cities

    result = [obj.to_dict() for obj in cities]

    return (jsonify(result))


@app_views.route('/cities/<string:city_id>',
                 methods=['GET'], strict_slashes=False)
def cities_get_id(city_id):
    """This method retrieve city by id"""
    city = storage.get(City, city_id)
    if (city is None):
        abort(404)
    result = city.to_dict()
    return (jsonify(result))


@app_views.route('/cities/<string:city_id>',
                 methods=['DELETE'], strict_slashes=False)
def city_delete(city_id):
    """This method delete city by id"""
    city_delete = storage.get(City, city_id)
    if city_delete is None:
        abort(404)
    else:
        city_delete.delete()
        storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/<string:state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def city_post(state_id):
    """This method add a new state"""
    if (not storage.get(State, state_id)):
        abort(404)

    new_data = request.get_json(silent=True)

    if (type(new_data) is dict):
        new_city = City(**new_data)
        setattr(new_city, "state_id", state_id)
        if (not storage.get(State, new_city.state_id)):
            abort(404)

        if (not new_city.to_dict().get('name', None)):
            return jsonify({'message': 'Missing name'}), 400

        new_city.save()
        return (jsonify(new_city.to_dict()), 201)

    return (jsonify({'message': 'Not a JSON'}), 400)


@app_views.route('/cities/<string:city_id>',
                 methods=['PUT'], strict_slashes=False)
def city_put(city_id):
    """This method update city by id"""
    find_city = storage.get(City, city_id)
    if (find_city is None):
        abort(404)

    update_city = request.get_json(silent=True)
    if (type(update_city) is dict):
        update_city.pop('id', None)
        update_city.pop('created_at', None)
        update_city.pop('updated_at', None)

        for key, value in update_city.items():
            setattr(find_city, key, value)
        find_city.save()
        return (jsonify(find_city.to_dict()), 200)

    return (jsonify({'message': 'Not a JSON'}), 400)
