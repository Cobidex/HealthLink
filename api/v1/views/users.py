#!/usr/bin/python3
'''module for user routes'''
from flask import jsonify, request
from api.v1.views import User_view
from models import storage
from models.user import User


@User_view.route('/users')
def GET_users():
    return jsonify([user.to_dict() for user in storage.all(User).values()])


@User_view.route('/users/<user_id>')
def GET_user(user_id):
    user = storage.get(User, user_id)

    if(user):
        return jsonify(user.to_dict())

    return jsonify({"Error": "Not found"}), 404


@User_view.route('/users/<user_id>', methods=['DELETE'])
def DELETE_user(user_id):
    user = storage.get(User, user_id)

    if (user):
        storage.delete(user)
        storage.save()
        return jsonify({})

    return jsonify({"Error": "Not found"}), 404


@User_view.route('/users', methods=['POST'])
def POST_user():
    req = request.get_json()

    if not req:
        return jsonify({"Error": "Not a JSON"}), 400
    if 'email' not in req:
        return jsonify({"Error": "missing email"}), 400
    if 'password' not in req:
        return jsonify({"Error": "Missing password"}), 400

    user = User(**req)
    user.save()
    return jsonify(user.to_dict())


@User_view.route('/users/<user_id>', methods=['PUT'])
def PUT_user(user_id):
    req = request.get_json()

    if not req:
        return jsonify({"Error": "Not a JSON"}), 400

    user = storage.get(User, user_id)
    if (user):
        for k, v in req.items():
            if k not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, k, v)
        storage.save()

        return jsonify(user.to_dict()), 200

    return jsonify({"Error": "Not found"}), 404
