#!/usr/bin/python3
'''module for hospital routes'''
from flask import Blueprint, jsonify, request
from api.v1.views import Hospital_view
import models
from models.city import City
from models.hospital import Hospital


@Hospital_view.route('/cities/<city_id>/hospitals')
def GET_hospitals(city_id):
    city_o = models.storage.get(City, city_id)

    if (city_o):
        hospitals = city_o.hospitals
        return jsonify([hospital.to_dict() for hospital in hospitals])

    return jsonify({"Error": "City not found"}), 404


@Hospital_view.route('/hospitals/<city_id>')
def GET_hospital(city_id):
    key = 'Hospital.{}'. format(city_id)

    if (models.storage.all(Hospital).get(key)):
        return jsonify(models.storage.all(Hospital).get(key).to_dict())
    else:
        return jsonify({"Error": "not found"}), 404


@Hospital_view.route('/hospitals/<city_id>', methods=['DELETE'])
def DELETE_hospital(city_id):
    key = 'Hospital.{}'. format(city_id)
    hospital = models.storage.all(Hospital)[key]

    if (hospital):
        models.storage.delete(hospital)
        models.storage.save()
        return jsonify({}), 200

    return jsonify({"Error": "not found"}), 404


@Hospital_view.route('/cities/<city_id>/hospitals', methods=['POST'])
def POST_hospital(city_id):
    city = models.storage.get(City, city_id)

    if (city):
        req = request.get_json()
        if not req:
            return jsonify({'message': 'Not a JSON'}), 400
        if 'name' not in req:
            return jsonify({'message': 'Missing name'}), 400
        if 'address' not in req:
            return jsonify({'message': 'Missing address'}), 400
        if 'phone_number' not in req:
            return jsonify({'message': 'Missing phone_number'}), 400
        if 'email' not in req:
            return jsonify({'message': 'Missing email'}), 400
        hospital = Hospital(**req)
        hospital.city_id = city_id
        hospital.save()
        return jsonify(hospital.to_dict()), 201

    return jsonify({"Error": "City not found"}), 404


@Hospital_view.route('/hospitals/<city_id>', methods=['PUT'])
def PUT_hospital(city_id):
    key = 'Hospital.{}'. format(city_id)
    hospital = models.storage.all(Hospital).get(key)

    if (hospital):
        req = request.get_json()
        if not req:
            return jsonify({'message': 'Not a JSON'}), 400
        for k, v in req.items():
            if k not in ['id', 'created_at',
                         'updated_at', 'city_id']:
                setattr(hospital, k, v)
        hospital.save()
        return jsonify(hospital.to_dict()), 200

    return jsonify({"Error": "not found"}), 404
