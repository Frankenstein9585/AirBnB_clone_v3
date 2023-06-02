#!/usr/bin/python3
"""This is the view for places"""
from flask import abort, request, jsonify, make_response

from models.city import City
from models.place import Place
from models.user import User
from api.v1.views import app_views
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Returns a list of all place objects"""
    city_key = 'City.{}'.format(city_id)
    if city_key not in storage.all(City):
        abort(404)
    return jsonify([value.to_dict() for value in
                    storage.all(Place).values()
                    if value.to_dict()['city_id'] == city_id]), 200


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Returns a specific place object based on its id"""
    try:
        place = storage.get(Place, place_id).to_dict()
        return jsonify(place)
    except AttributeError:
        abort(404)
    except KeyError:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a place object"""
    place_key = 'Place.{}'.format(place_id)
    if place_key not in storage.all(Place):
        abort(404)
    storage.delete(storage.get(Place, place_id))
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Creates a new place object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    data['city_id'] = city_id

    if not request.is_json:
        abort(make_response(jsonify({'error': 'Not a JSON'}), 400))

    if 'user_id' not in data:
        abort(make_response(jsonify({'error': 'Missing user_id'}), 400))
    else:
        if 'User.{}'.format(data['user_id']) not in storage.all(User):
            abort(404)

    if 'name' not in data:
        abort(make_response(jsonify({'error': 'Missing name'}), 400))

    place = Place()
    for key, value in data.items():
        setattr(place, key, value)
    place.save()
    storage.new(place)
    storage.save()

    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a place object"""

    data = request.get_json()
    if not data:
        abort(make_response(jsonify({'error': 'Not a JSON'}), 400))

    # if 'name' not in data:
    #     abort(make_response(jsonify({'error': 'Missing name'}), 400))

    place = storage.get(Place, place_id)
    keys_ignore = ['id', 'created_at', 'updated_at', 'user_id', 'city_id']

    if not place:
        abort(404)

    for key, value in data.items():
        if key not in keys_ignore:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
