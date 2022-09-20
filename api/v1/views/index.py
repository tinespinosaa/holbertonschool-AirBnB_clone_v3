#!/usr/bin/python3
"""route /status"""
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.user import User
from models.city import City
from models.review import Review
from models.state import State
from models.place import Place
from models import storage


@app_views.route('/status')
def status():
    """"""
    obj_res = {
        "status": "OK"
    }

    return (jsonify(obj_res))


@app_views.route('/stats')
def stats():
    """"""
    obj_res = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }

    return (jsonify(obj_res))
