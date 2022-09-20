#!/usr/bin/python3
"""new view for Users objects that handles
all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def users_get():
    """This method retrieve list of all users"""
    users = storage.all(User)
    if (users is None):
        abort(404)

    iterable_users = users.values()

    result = [obj.to_dict() for obj in iterable_users]

    return (jsonify(result))


@app_views.route('/users/<string:user_id>',
                 methods=['GET'], strict_slashes=False)
def user_get_id(user_id):
    """This method retrieve user by id"""
    user = storage.get(User, user_id)
    if (user is None):
        abort(404)
    result = user.to_dict()
    return (jsonify(result))


@app_views.route('/users/<string:user_id>',
                 methods=['DELETE'], strict_slashes=False)
def user_delete(user_id):
    """This method delete user by id"""
    user_delete = storage.get(User, user_id)
    if user_delete is None:
        abort(404)
    else:
        user_delete.delete()
        storage.save()
    return (jsonify({}), 200)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def user_post():
    """This method add a new user"""
    new_data = request.get_json(silent=True)

    if (type(new_data) is dict):
        new_user = User(**new_data)
        if (not new_user.to_dict().get('email', None)):
            return jsonify({'message': 'Missing name'}), 400
        if (not new_user.to_dict().get('password', None)):
            return jsonify({'message': 'Missing name'}), 400

        new_user.save()
        return (jsonify(new_user.to_dict()), 201)

    return (jsonify({'message': 'Not a JSON'}), 400)


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def user_put(user_id):
    """This method update user by id"""
    find_user = storage.get(User, user_id)
    if (find_user is None):
        abort(404)

    update_user = request.get_json(silent=True)
    if (type(update_user) is dict):
        update_user.pop('id', None)
        update_user.pop('created_at', None)
        update_user.pop('updated_at', None)

        for key, value in update_user.items():
            setattr(find_user, key, value)
        find_user.save()
        return (jsonify(find_user.to_dict()), 200)

    return (jsonify({'message': 'Not a JSON'}), 400)

