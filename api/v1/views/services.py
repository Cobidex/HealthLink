#!/usr/bin/python3
'''module for service routes'''
from flask import Blueprint, jsonify, request
from api.v1.views import Service_view
import models
from models.service import Service


@Service_view.route('/services')
def services():
    services = models.storage.all(Service)
    return jsonify([service.to_dict() for service in services.values()])


@Service_view.route('/services/<service_id>')
def service_id(service_id):
    key = 'Service.{}'. format(service_id)

    if (models.storage.all(Service).get(key)):
        return jsonify(models.storage.all(Service).get(key).to_dict())
    else:
        return jsonify({"Error": "not found"}), 404


@Service_view.route('/services/<service_id>', methods=['DELETE'])
def delete(service_id):
    service = models.storage.get(Service, service_id)

    if (service):
        models.storage.delete(service)
        models.storage.save()
        return jsonify({}), 200

    return jsonify({"Error": "not found"}), 404


@Service_view.route('/services', methods=['POST'])
def make():
    req = request.get_json()

    if not req:
        return jsonify({'message': 'Not a JSON'}), 400
    if 'name' not in req:
        return jsonify({'message': 'Missing name'}), 400
    service = Service(**req)
    service.save()
    return jsonify(service.to_dict()), 201


@Service_view.route('/services/<service_id>', methods=['PUT'])
def up_date(service_id):
    key = 'Service.{}'. format(service_id)
    service = models.storage.all(Service).get(key)

    if (service):
        req = request.get_json()
        if not req:
            return jsonify({'message': 'Not a JSON'}), 400
        for k, v in req.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(service, k, v)
        service.save()
        return jsonify(service.to_dict()), 200

    return jsonify({"Error": "not found"}), 404
