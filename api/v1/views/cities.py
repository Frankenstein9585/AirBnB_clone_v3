#!/usr/bin/python3
"""This is the view for cities"""
from flask import abort, request, jsonify, make_response

from models.state import State
from models.city import City
from api.v1.views import app_views
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Returns a list of all city objects"""
    state_key = 'State.{}'.format(state_id)
    if state_key not in storage.all(State):
        abort(404)
    return jsonify([value.to_dict() for value in
                    storage.all(City).values()
                    if value.to_dict()['state_id'] == state_id]), 200


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Returns a specific city object based on its id"""
    try:
        city = storage.get(City, city_id).to_dict()
        return jsonify(city)
    except AttributeError:
        abort(404)
    except KeyError:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a city object"""
    city_key = 'City.{}'.format(city_id)
    if city_key not in storage.all(City):
        abort(404)
    storage.delete(storage.get(City, city_id))
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Creates a new city object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    data['state_id'] = state_id

    if not data:
        abort(make_response(jsonify({'error': 'Not a JSON'}), 400))

    if 'name' not in data:
        abort(make_response(jsonify({'error': 'Missing name'}), 400))

    city = City()
    for key, value in data.items():
        setattr(city, key, value)
    city.save()
    storage.new(city)
    storage.save()

    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a city object"""

    data = request.get_json()
    if not data:
        abort(make_response(jsonify({'error': 'Not a JSON'}), 400))

    if 'name' not in data:
        abort(make_response(jsonify({'error': 'Missing name'}), 400))

    city = storage.get(City, city_id)
    keys_ignore = ['id', 'created_at', 'updated_at']

    if not city:
        abort(404)

    for key, value in data.items():
        if key not in keys_ignore:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
