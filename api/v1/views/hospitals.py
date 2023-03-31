#!/usr/bin/python3
'''module for hospital routes'''
from flask import Blueprint, jsonify, request
from api.v1.views import Hospital_view
import models
from models.state import State
from models.city import City
from models.hospital import Hospital
from models.service import Service


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


@Hospital_view.route('/hospitals_search', methods=['POST'])
def SEARCH_hospitals():
    if request.is_json:
        req_dict = request.get_json()
    else:
        return (jsonify({'error': 'Not a JSON'}), 400)

    # complile list of all cities for named states + individually named cities
    city_list = []
    if 'states' in req_dict:
        for state_id in req_dict['states']:
            state = models.storage.get(State, state_id)
            if state:
                for city in state.cities:
                    city_list.append(city)

    if 'cities' in req_dict:
        for city_id in req_dict['cities']:
            city = models.storage.get(City, city_id)
            if city:
                if city not in city_list:
                    city_list.append(city)

    # list all hospitals to be found in those cities
    hospital_list = []
    for city in city_list:
        for hospital in city.hospitals:
            hospital_list.append(hospital)

    # if no states or cities with valid ids provided, defaults to all hospitals
    if len(hospital_list) == 0:
        for hospital in models.storage.all(Hospital).values():
            hospital_list.append(hospital)

    # filter hospitals to only include those that share all listed services
    service_list = []
    if 'services' in req_dict:
        for service_id in req_dict['services']:
            service = models.storage.get(Service, service_id)
            if service:
                service_list.append(service)

        filtered_hospital_list = hospital_list.copy()
        for hospital in hospital_list:
            if not all(service in hospital.services for service in service_list):
                filtered_hospital_list.remove(hospital)
        hospital_list = filtered_hospital_list

    # prepare return list
    hospital_dict_list = []
    for hospital in hospital_list:
        hospital_dict = hospital.to_dict()
        if 'services' in hospital_dict:
            del hospital_dict['services']
        hospital_dict_list.append(hospital_dict)

    return jsonify(hospital_dict_list)


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
