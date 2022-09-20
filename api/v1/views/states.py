#!/usr/bin/python3
"""new view for States objects that handles
all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def state_get():
    """This method retrieve list of all states"""
    data_states = storage.all(State).values()
    result = [obj.to_dict() for obj in data_states]

    return (jsonify(result))


@app_views.route('/states/<string:state_id>',
                 methods=['GET'], strict_slashes=False)
def state_get_id(state_id):
    """This method retrieve list of all states by id"""
    state = storage.get(State, state_id)
    if (state is None):
        abort(404)
    result = state.to_dict()
    return (jsonify(result))


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def state_post():
    """This method add a new state"""
    new_data = request.get_json(silent=True)

    if (type(new_data) is dict):
        new_state = State(**new_data)
        if (not new_state.to_dict().get('name', None)):
            return jsonify({'message': 'Missing name'}), 400
        new_state.save()
        return (jsonify(new_state.to_dict()), 201)

    return (jsonify({'message': 'Not a JSON'}), 400)


@app_views.route('/states/<string:state_id>',
                 methods=['PUT'], strict_slashes=False)
def state_put(state_id):
    """This method update state by id"""
    find_state = storage.get(State, state_id)
    if (find_state is None):
        abort(404)

    update_state = request.get_json(silent=True)
    if (type(update_state) is dict):
        update_state.pop('id', None)
        update_state.pop('created_at', None)
        update_state.pop('updated_at', None)

        for key, value in update_state.items():
            setattr(find_state, key, value)
        find_state.save()
        return (jsonify(find_state.to_dict()), 200)

    return (jsonify({'message': 'Not a JSON'}), 400)


@app_views.route('/states/<string:state_id>',
                 methods=['DELETE'], strict_slashes=False)
def state_delete(state_id):
    """This method delete state by id"""
    state_delete = storage.get(State, state_id)
    if state_delete is None:
        abort(404)
    else:
        state_delete.delete()
        storage.save()
    return (jsonify({}), 200)
