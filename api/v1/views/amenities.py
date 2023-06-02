#!/usr/bin/python3
"""This is the view for amenities"""
from flask import abort, request, jsonify, make_response

from models.amenity import Amenity
from api.v1.views import app_views
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Returns a list of all amenity objects"""
    return jsonify([amenity.to_dict() for
                    amenity in storage.all(Amenity).values()]), 200


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Returns a specific amenity object based on its id"""
    try:
        amenity = storage.get(Amenity, amenity_id).to_dict()
        return jsonify(amenity)
    except AttributeError:
        abort(404)
    except KeyError:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an Amenity object"""
    amenity_key = 'Amenity.{}'.format(amenity_id)
    if amenity_key not in storage.all(Amenity):
        abort(404)
    storage.delete(storage.get(Amenity, amenity_id))
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Creates a new Amenity object"""
    data = request.get_json()

    if not data:
        abort(make_response(jsonify({'error': 'Not a JSON'}), 400))

    if 'name' not in data:
        abort(make_response(jsonify({'error': 'Missing name'}), 400))

    amenity = Amenity(**data)
    amenity.save()
    storage.new(amenity)
    storage.save()
    # storage.all()['Amenity.{}'.format(amenity.id)] = amenity
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates a Amenity object"""
    # amenity_key = 'Amenity.{}'.format(amenity_id)
    # amenity = amenities[amenity_key]
    # if amenity_key not in amenities:
    #     abort(404)
    #
    # data = request.get_json()
    #
    # if not data:
    #     abort(400, 'Not a JSON')
    #
    # data.pop('id', None)
    # data.pop('created_at', None)
    # data.pop('updated_at', None)
    #
    # for key, value in data.items():
    #     setattr(amenity, key, value)
    #
    # amenity.save()
    # return jsonify(amenity.to_dict()), 200
    data = request.get_json()
    if not data:
        abort(make_response(jsonify({'error': 'Not a JSON'}), 400))

    if 'name' not in data:
        abort(make_response(jsonify({'error': 'Missing name'}), 400))

    amenity = storage.get(Amenity, amenity_id)
    keys_ignore = ['id', 'created_at', 'updated_at']

    if amenity:
        for key, value in data.items():
            if key not in keys_ignore:
                setattr(amenity, key, value)
        amenity.save()
        # storage.all(Amenity)[amenity_key] = amenity
        return jsonify(amenity.to_dict()), 200
    abort(404)
