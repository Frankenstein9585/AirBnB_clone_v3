#!/usr/bin/python3
"""This is the view for users"""
from flask import abort, request, jsonify, make_response

from models.user import User
from api.v1.views import app_views
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Returns a list of all user objects"""
    return jsonify([user.to_dict() for
                    user in storage.all(User).values()]), 200


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Returns a specific user object based on its id"""
    try:
        user = storage.get(User, user_id).to_dict()
        return jsonify(user)
    except AttributeError:
        abort(404)
    except KeyError:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user_key = 'User.{}'.format(user_id)
    if user_key not in storage.all(User):
        abort(404)
    storage.delete(storage.get(User, user_id))
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Creates a new User object"""
    data = request.get_json()

    if not data:
        abort(make_response(jsonify({'error': 'Not a JSON'}), 400))

    if 'email' not in data:
        abort(make_response(jsonify({'error': 'Missing email'}), 400))

    if 'password' not in data:
        abort(make_response(jsonify({'error': 'Missing password'}), 400))

    user = User(**data)
    user.save()
    storage.new(user)
    storage.save()
    # storage.all()['User.{}'.format(user.id)] = user
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    # user_key = 'User.{}'.format(user_id)
    # user = users[user_key]
    # if user_key not in users:
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
    #     setattr(user, key, value)
    #
    # user.save()
    # return jsonify(user.to_dict()), 200
    data = request.get_json()
    if not data:
        abort(make_response(jsonify({'error': 'Not a JSON'}), 400))

    user = storage.get(User, user_id)
    keys_ignore = ['id', 'created_at', 'updated_at', 'email']

    if user:
        for key, value in data.items():
            if key not in keys_ignore:
                setattr(user, key, value)
        user.save()
        # storage.all(User)[user_key] = user
        return jsonify(user.to_dict()), 200
    abort(404)
