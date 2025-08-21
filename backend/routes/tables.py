from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from mongoengine import NotUniqueError
from datetime import datetime
from models import Table, Reservation

tables = Blueprint('tables', __name__)

# --------- Tables CRUD ---------

@tables.route('/tables', methods=['POST'])
@jwt_required()
def create_table():
    data = request.get_json() or {}
    number = (data.get('number') or '').strip()
    seats = data.get('seats', 4)

    if not number:
        return jsonify({"msg": "กรุณาระบุเลขโต๊ะ"}), 400

    try:
        t = Table(number=number, seats=seats, is_active=True).save()
        return jsonify({
            "id": str(t.id),
            "number": t.number,
            "seats": t.seats,
            "isActive": t.is_active
        }), 201
    except NotUniqueError:
        return jsonify({"msg": "เลขโต๊ะนี้มีอยู่แล้ว"}), 400

@tables.route('/tables', methods=['GET'])
@jwt_required()
def list_tables():
    docs = Table.objects().order_by('number')
    return jsonify([{
        "id": str(d.id),
        "number": d.number,
        "seats": d.seats,
        "isActive": d.is_active
    } for d in docs]), 200

@tables.route('/tables/<table_id>', methods=['GET'])
@jwt_required()
def get_table(table_id):
    t = Table.objects(id=table_id).first()
    if not t:
        return jsonify({"msg": "ไม่พบโต๊ะ"}), 404
    return jsonify({
        "id": str(t.id),
        "number": t.number,
        "seats": t.seats,
        "isActive": t.is_active
    }), 200

@tables.route('/tables/<table_id>', methods=['PATCH'])
@jwt_required()
def update_table(table_id):
    data = request.get_json() or {}
    t = Table.objects(id=table_id).first()
    if not t:
        return jsonify({"msg": "ไม่พบโต๊ะ"}), 404
    if 'number' in data:
        t.number = (data['number'] or '').strip()
    if 'seats' in data:
        t.seats = int(data['seats'])
    if 'isActive' in data:
        t.is_active = bool(data['isActive'])
    try:
        t.save()
        return jsonify({"msg": "updated"}), 200
    except NotUniqueError:
        return jsonify({"msg": "เลขโต๊ะนี้มีอยู่แล้ว"}), 400

@tables.route('/tables/<table_id>', methods=['DELETE'])
@jwt_required()
def delete_table(table_id):
    t = Table.objects(id=table_id).first()
    if not t:
        return jsonify({"msg": "ไม่พบโต๊ะ"}), 404
    # ป้องกันลบถ้ามีการจองอยู่ (เปิดใช้ถ้าต้องการ)
    # if Reservation.objects(table=t, status__in=["reserved","seated"]).first():
    #     return jsonify({"msg":"โต๊ะนี้มีการจองอยู่ ลบไม่ได้"}), 400
    t.delete()
    return jsonify({"msg": "deleted"}), 200

# --------- Activate / Deactivate (แก้ CORS preflight 404) ---------

# Preflight OPTIONS ควรตอบ 204 โดยไม่ต้อง JWT
@tables.route('/tables/<table_id>/activate', methods=['OPTIONS'])
def options_activate_table(table_id):
    return ('', 204)

@tables.route('/tables/<table_id>/deactivate', methods=['OPTIONS'])
def options_deactivate_table(table_id):
    return ('', 204)

@tables.route('/tables/<table_id>/activate', methods=['PATCH'])
@jwt_required()
def activate_table(table_id):
    t = Table.objects(id=table_id).first()
    if not t:
        return jsonify({"msg": "ไม่พบโต๊ะ"}), 404
    t.is_active = True
    t.save()
    return jsonify({"msg": "activated", "id": str(t.id), "isActive": t.is_active}), 200

@tables.route('/tables/<table_id>/deactivate', methods=['PATCH'])
@jwt_required()
def deactivate_table(table_id):
    t = Table.objects(id=table_id).first()
    if not t:
        return jsonify({"msg": "ไม่พบโต๊ะ"}), 404
    t.is_active = False
    t.save()
    return jsonify({"msg": "deactivated", "id": str(t.id), "isActive": t.is_active}), 200

# --------- Stats (เผื่อ Dashboard เรียกอยู่) ---------

@tables.route('/tables/stats', methods=['GET'])
@jwt_required()
def tables_stats():
    tables = Table.objects()
    total = tables.count()
    available = tables.filter(is_active=True).count()

    now = datetime.utcnow()
    # occupied: มีสถานะ seated หรือซ้อนเวลาปัจจุบัน
    resvs = Reservation.objects(status__in=["reserved", "seated"]).only(
        'status', 'reserve_start', 'reserve_end'
    )
    occupied = 0
    reserved = 0
    for r in resvs:
        if r.status == "seated" or (r.reserve_start and r.reserve_end and r.reserve_start <= now <= r.reserve_end):
            occupied += 1
        if r.status == "reserved":
            reserved += 1

    return jsonify({
        "total": total,
        "available": available,
        "occupied": occupied,
        "reserved": reserved
    }), 200
