#!/usr/bin/python3
"""This is the view for states"""
from flask import abort, request, jsonify, make_response

from models.state import State
from api.v1.views import app_views
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Returns a list of all state objects"""
    return jsonify([state.to_dict() for
                    state in storage.all(State).values()]), 200


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """Returns a specific state object based on its id"""
    try:
        state = storage.get(State, state_id).to_dict()
        return jsonify(state)
    except AttributeError:
        abort(404)
    except KeyError:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    state_key = 'State.{}'.format(state_id)
    if state_key not in storage.all(State):
        abort(404)
    storage.delete(storage.get(State, state_id))
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Creates a new State object"""
    data = request.get_json()

    if not data:
        abort(make_response(jsonify({'error': 'Not a JSON'}), 400))

    if 'name' not in data:
        abort(make_response(jsonify({'error': 'Missing name'}), 400))

    state = State(**data)
    state.save()
    storage.new(state)
    storage.save()
    # storage.all()['State.{}'.format(state.id)] = state
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    # state_key = 'State.{}'.format(state_id)
    # state = states[state_key]
    # if state_key not in states:
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
    #     setattr(state, key, value)
    #
    # state.save()
    # return jsonify(state.to_dict()), 200
    data = request.get_json()
    if not data:
        abort(make_response(jsonify({'error': 'Not a JSON'}), 400))

    if 'name' not in data:
        abort(make_response(jsonify({'error': 'Missing name'}), 400))

    state = storage.get(State, state_id)
    keys_ignore = ['id', 'created_at', 'updated_at']

    if state:
        for key, value in data.items():
            if key not in keys_ignore:
                setattr(state, key, value)
        state.save()
        # storage.all(State)[state_key] = state
        return jsonify(state.to_dict()), 200
    abort(404)
