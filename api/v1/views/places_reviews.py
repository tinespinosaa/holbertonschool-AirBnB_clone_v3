#!/usr/bin/python3
"""new view for Reviews objects that handles
all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
from models import storage


@app_views.route('places/<string:place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def reviews_get_from_places(place_id):
    """This method retrieve list of all reviews by place"""
    place = storage.get(Place, place_id)
    if (place is None):
        abort(404)

    reviews = place.reviews
    if (reviews is None):
        abort(404)

    result = [obj.to_dict() for obj in reviews]

    return (jsonify(result))


@app_views.route('/reviews/<string:review_id>',
                 methods=['GET'], strict_slashes=False)
def reviews_get_id(review_id):
    """This method retrieve review by id"""
    review = storage.get(Review, review_id)
    if (review is None):
        abort(404)
    result = review.to_dict()
    return (jsonify(result))


@app_views.route('/reviews/<string:review_id>',
                 methods=['DELETE'], strict_slashes=False)
def review_delete(review_id):
    """This method delete review by id"""
    review_delete = storage.get(Review, review_id)
    if review_delete is None:
        abort(404)
    else:
        review_delete.delete()
        storage.save()
    return (jsonify({}), 200)


@app_views.route('/places/<string:place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def review_post(place_id):
    """This method add a new review in place by id"""
    if (not storage.get(Place, place_id)):
        abort(404)

    new_data = request.get_json(silent=True)

    if (type(new_data) is dict):
        new_review = Review(**new_data)
        setattr(new_review, "place_id", place_id)

        user_id = new_review.to_dict().get('user_id', None)
        if (not user_id):
            return jsonify({'message': 'Missing user_id'}), 400
        if (not storage.get(User, user_id)):
            abort(404)

        if (not new_review.to_dict().get('text', None)):
            return jsonify({'message': 'Missing text'}), 400

        new_review.save()
        return (jsonify(new_review.to_dict()), 201)

    return (jsonify({'message': 'Not a JSON'}), 400)


@app_views.route('/reviews/<string:review_id>',
                 methods=['PUT'], strict_slashes=False)
def review_put(review_id):
    """This method update review by id"""
    find_review = storage.get(Review, review_id)
    if (find_review is None):
        abort(404)

    update_review = request.get_json(silent=True)
    if (type(update_review) is dict):
        update_review.pop('id', None)
        update_review.pop('user_id', None)
        update_review.pop('place_id', None)
        update_review.pop('created_at', None)
        update_review.pop('updated_at', None)

        for key, value in update_review.items():
            setattr(find_review, key, value)
        find_review.save()
        return (jsonify(find_review.to_dict()), 200)

    return (jsonify({'message': 'Not a JSON'}), 400)
