from flask import Blueprint, request, jsonify
from firebase_config import db
import uuid

activity_bp = Blueprint('activity', __name__)

#สร้างกิจกรรม
@activity_bp.route('/activity', methods=['POST'])
def add_activity():
    data = request.json
    activity_id = str(uuid.uuid4())
    db.collection('activities').document(activity_id).set({
        'plant_id': data['plant_id'],
        'activity_date' : data['activity_date'],
        'activity_type': data['activity_type'],
    })
    return jsonify({'message': 'เพิ่มกิจกรรมสำเร็จ', 'id': activity_id}), 201

#ดูกิจกรรรม
@activity_bp.route('/activities', methods=['GET'])
def get_activities():
    docs = db.collection('activities').stream()
    activities = []
    for doc in docs:
        activity = doc.to_dict()
        activity['id'] = doc.id
        activities.append(activity)
    return jsonify(activities)
    
#แก้ไข
@activity_bp.route('/activity/<activity_id>', methods=['PUT'])
def update_activity(activity_id):
    date = request.json
    db.collection('activities').document(id).update({
        'activity_date': date['activity_date'],
        'activity_type': date['activity_type'],
    })
    return jsonify({'message': 'แก้ไขกิจกรรมสำเร็จ'})

#ลบก
@activity_bp.route('/activity/<activity_id>', methods=['DELETE'])
def delete_activity(activity_id):
    db.collection('activities').document(id).delete()
    return jsonify({'message': 'ลบกิจกรรมสำเร็จ'})