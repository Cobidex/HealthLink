#!/usr/bin/python3
'''module for user routes'''
from flask import Blueprint, jsonify, request
from api.v1.views import State_view
import models
from models.state import State


@State_view.route('/states')
def GET_states():
    states = models.storage.all(State)
    return jsonify([state.to_dict() for state in states.values()])


@State_view.route('/states/<name>')
def GET_states_name(name):
    states = models.storage.all(State)
    if type(name) == str:
        return jsonify([state.to_dict() for state in states.values() if state.name == name])
    return jsonify({"Error": "state name must be string"}), 404


@State_view.route('/states/<state_id>')
def GET_state(state_id):
    key = 'State.{}'. format(state_id)
    if (models.storage.all(State).get(key)):
        return jsonify(models.storage.all(State).get(key).to_dict())
    else:
        return jsonify({"Error": "not found"}), 404


@State_view.route('/states/<state_id>', methods=['DELETE'])
def DELETE_state(state_id):
    key = 'State.{}'. format(state_id)
    state = models.storage.all(State)[key]

    if (state):
        models.storage.delete(state)
        models.storage.save()
        return jsonify({}), 200

    return jsonify({"Error": "not found"}), 404


@State_view.route('/states', methods=['POST'])
def POST_state():
    req = request.get_json()

    if not req:
        return jsonify({'message': 'Not a JSON'}), 400
    if 'name' not in req:
        return jsonify({'message': 'Missing name'}), 400
    state = State(**req)
    state.save()
    return jsonify(state.to_dict()), 201


@State_view.route('/states/<state_id>', methods=['PUT'])
def PUT_state(state_id):
    key = 'State.{}'. format(state_id)
    state = models.storage.all(State).get(key)

    if (state):
        req = request.get_json()
        if not req:
            return jsonify({'message': 'Not a JSON'}), 400
        for k, v in req.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(state, k, v)
        state.save()
        return jsonify(state.to_dict()), 200

    return jsonify({"Error": "not found"}), 404
