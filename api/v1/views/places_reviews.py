#!/usr/bin/python3
"""This is the view for reviews"""
from flask import abort, request, jsonify, make_response

from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Returns a list of all review objects"""
    place_key = 'Place.{}'.format(place_id)
    if place_key not in storage.all(Place):
        abort(404)
    return jsonify([value.to_dict() for value in
                    storage.all(Review).values()
                    if value.to_dict()['place_id'] == place_id]), 200


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Returns a specific review object based on its id"""
    try:
        review = storage.get(Review, review_id).to_dict()
        return jsonify(review)
    except AttributeError:
        abort(404)
    except KeyError:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a review object"""
    review_key = 'Review.{}'.format(review_id)
    if review_key not in storage.all(Review):
        abort(404)
    storage.delete(storage.get(Review, review_id))
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """Creates a new review object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    data['place_id'] = place_id

    if not request.is_json:
        abort(make_response(jsonify({'error': 'Not a JSON'}), 400))

    if 'user_id' not in data:
        abort(make_response(jsonify({'error': 'Missing user_id'}), 400))
    else:
        if 'User.{}'.format(data['user_id']) not in storage.all(User):
            abort(404)

    if 'text' not in data:
        abort(make_response(jsonify({'error': 'Missing text'}), 400))

    review = Review()
    for key, value in data.items():
        setattr(review, key, value)
    review.save()
    storage.new(review)
    storage.save()

    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a review object"""

    data = request.get_json()
    if not data:
        abort(make_response(jsonify({'error': 'Not a JSON'}), 400))

    # if 'name' not in data:
    #     abort(make_response(jsonify({'error': 'Missing name'}), 400))

    review = storage.get(Review, review_id)
    keys_ignore = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']

    if not review:
        abort(404)

    for key, value in data.items():
        if key not in keys_ignore:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
