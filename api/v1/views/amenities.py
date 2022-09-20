#!/usr/bin/python3
"""new view for Amenities objects that handles
all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def amenities_get():
    """This method retrieve list of all amenities"""
    amenities = storage.all(Amenity)
    if (amenities is None):
        abort(404)

    iterable_amenities = amenities.values()

    result = [obj.to_dict() for obj in iterable_amenities]

    return (jsonify(result))


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['GET'], strict_slashes=False)
def amenity_get_id(amenity_id):
    """This method retrieve amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if (amenity is None):
        abort(404)
    result = amenity.to_dict()
    return (jsonify(result))


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def amenity_delete(amenity_id):
    """This method delete amenity by id"""
    amenity_delete = storage.get(Amenity, amenity_id)
    if amenity_delete is None:
        abort(404)
    else:
        amenity_delete.delete()
        storage.save()
    return (jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def amenity_post():
    """This method add a new amenity"""
    new_data = request.get_json(silent=True)

    if (type(new_data) is dict):
        new_amenity = Amenity(**new_data)

        if (not new_amenity.to_dict().get('name', None)):
            return jsonify({'message': 'Missing name'}), 400

        new_amenity.save()
        return (jsonify(new_amenity.to_dict()), 201)

    return (jsonify({'message': 'Not a JSON'}), 400)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def amenity_put(amenity_id):
    """This method update city by id"""
    find_amenity = storage.get(Amenity, amenity_id)
    if (find_amenity is None):
        abort(404)

    update_amenity = request.get_json(silent=True)
    if (type(update_amenity) is dict):
        update_amenity.pop('id', None)
        update_amenity.pop('created_at', None)
        update_amenity.pop('updated_at', None)

        for key, value in update_amenity.items():
            setattr(find_amenity, key, value)
        find_amenity.save()
        return (jsonify(find_amenity.to_dict()), 200)

    return (jsonify({'message': 'Not a JSON'}), 400)
