#!/usr/bin/python3
'''module for reviews routes'''
from flask import Blueprint, jsonify, request
from api.v1.views import Review_view
import models
from models.hospital import Hospital
from models.review import Review


@Review_view.route('/hospitals/<hospital_id>/reviews')
def GET_reviews(hospital_id):
    hospital = models.storage.get(Hospital, hospital_id)

    if (hospital):
        reviews = hospital.reviews
        return jsonify([review.to_dict() for review in reviews])
    return jsonify({"Error": "Hospital not found"}), 404


@Review_view.route('/reviews/<review_id>')
def GET_review(review_id):
    key = 'Review.{}'. format(review_id)
    if (models.storage.all(Review).get(key)):
        return jsonify(models.storage.all(Review).get(key).to_dict())
    else:
        return jsonify({"Error": "not found"}), 404


@Review_view.route('/reviews/<review_id>', methods=['DELETE'])
def DELETE_review(review_id):
    key = 'Review.{}'. format(review_id)
    review = models.storage.all(Review)[key]
    if (review):
        models.storage.delete(ob)
        models.storage.save()
        return jsonify({}), 200
    return jsonify({"Error": "not found"}), 404


@Review_view.route('/hospitals/<hospital_id>/reviews', methods=['POST'])
def POST_review(hospital_id):
    hospital = models.storage.get(Hospital, hospital_id)

    if (hospital):
        req = request.get_json()
        if not req:
            return jsonify({'message': 'Not a JSON'}), 400
        if 'text' not in req:
            return jsonify({'message': 'Missing text'}), 400
        if 'user_id' not in req:
            return jsonify({'message': 'Missing user_id'}), 400
        review = Review(**req)
        review.hospital_id = hospital_id
        review.save()
        return jsonify(review.to_dict()), 201

    return jsonify({"Error": "Hospital not found"}), 404


@Review_view.route('/reviews/<review_id>', methods=['PUT'])
def PUT_review(review_id):
    key = 'Review.{}'. format(review_id)
    review = models.storage.all(Review).get(key)

    if (review):
        req = request.get_json()
        if not req:
            return jsonify({'message': 'Not a JSON'}), 400
        for k, v in req.items():
            if k not in ['id', 'created_at',
                         'updated_at', 'user_id', 'hospital_id']:
                setattr(review, k, v)
        review.save()
        return jsonify(review.to_dict()), 200

    return jsonify({"Error": "not found"}), 404
