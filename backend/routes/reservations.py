from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from models import Reservation, Table, User

reservations = Blueprint('reservations', __name__)

def parse_dt(s: str):
    """รองรับค่า datetime-local (YYYY-MM-DDTHH:MM) และ ISO format"""
    if not s:
        return None
    try:
        if len(s) == 16:  # YYYY-MM-DDTHH:MM
            return datetime.strptime(s, "%Y-%m-%dT%H:%M")
        return datetime.fromisoformat(s)
    except Exception:
        return None

def serialize_reservation(doc: Reservation):
    """แปลง Reservation เป็น dict สำหรับส่งออก API"""
    return {
        "id": str(doc.id),
        "customerName": doc.customer_name,
        "phone": doc.phone,
        "partySize": doc.party_size,
        "table": {
            "id": str(doc.table.id) if doc.table else None,
            "number": doc.table.number if doc.table else None,
            "seats": doc.table.seats if doc.table else None,
            "isActive": doc.table.is_active if doc.table else None,
        } if doc.table else None,
        "reserveStart": doc.reserve_start.isoformat() if doc.reserve_start else None,
        "reserveEnd": doc.reserve_end.isoformat() if doc.reserve_end else None,
        "status": doc.status,
        "userId": str(doc.user.id) if doc.user else None,
        "createdAt": doc.created_at.isoformat() if getattr(doc, "created_at", None) else None,
        "updatedAt": doc.updated_at.isoformat() if getattr(doc, "updated_at", None) else None,
    }

@reservations.route('/reservations', methods=['GET'])
@jwt_required()
def list_reservations():
    user_id = get_jwt_identity()
    user = User.objects(id=user_id).first()
    if not user:
        return jsonify({"msg": "Unauthorized"}), 401

    qs = Reservation.objects(user=user).order_by('-reserve_start')
    return jsonify([serialize_reservation(d) for d in qs]), 200

@reservations.route('/reservations', methods=['POST'])
@jwt_required()
def create_reservation():
    user_id = get_jwt_identity()
    user = User.objects(id=user_id).first()
    if not user:
        return jsonify({"msg": "Unauthorized"}), 401

    data = request.get_json() or {}
    customer_name = (data.get('customerName') or '').strip()
    phone = (data.get('phone') or '').strip()
    party_size = int(data.get('partySize') or 1)

    reserve_start = parse_dt(data.get('reserveStart'))
    reserve_end = parse_dt(data.get('reserveEnd'))
    if reserve_start and not reserve_end:
        reserve_end = reserve_start + timedelta(minutes=int(data.get('reserveDurationMinutes') or 120))

    table_id = data.get('tableId')
    table_number = (data.get('tableNumber') or '').strip()

    if not (customer_name and party_size and reserve_start and (table_id or table_number)):
        return jsonify({"msg": "ข้อมูลไม่ครบ customerName/partySize/reserveStart/table"}), 400

    table = None
    if table_id:
        table = Table.objects(id=table_id).first()
    elif table_number:
        table = Table.objects(number=table_number).first()

    if not table:
        return jsonify({"msg": "ไม่พบโต๊ะ โปรดเพิ่มโต๊ะก่อน"}), 400
    if not table.is_active:
        return jsonify({"msg": "โต๊ะนี้ถูกปิดใช้งาน"}), 400

    # ถ้าไม่ได้ส่ง reserve_end มาต้องคำนวณแล้วถึงเช็ค overlap (ทำข้างบนแล้ว)
    if not reserve_end:
        return jsonify({"msg": "กำหนดเวลาสิ้นสุดไม่ถูกต้อง"}), 400

    # กันเวลาคาบเกี่ยว
    conflict = Reservation.objects(
        table=table,
        status__in=["reserved", "seated"],
        reserve_start__lt=reserve_end,
        reserve_end__gt=reserve_start
    ).first()
    if conflict:
        return jsonify({"msg": "ช่วงเวลานี้โต๊ะถูกจองแล้ว"}), 409

    doc = Reservation(
        customer_name=customer_name,
        phone=phone,
        party_size=party_size,
        table=table,
        reserve_start=reserve_start,
        reserve_end=reserve_end,
        status=data.get('status') or "reserved",
        user=user
    )
    try:
        doc.save()
        return jsonify(serialize_reservation(doc)), 201
    except Exception as e:
        return jsonify({"msg": f"บันทึกล้มเหลว: {e}"}), 400

@reservations.route('/reservations/<resv_id>', methods=['GET'])
@jwt_required()
def get_reservation(resv_id):
    user_id = get_jwt_identity()
    user = User.objects(id=user_id).first()
    if not user:
        return jsonify({"msg": "Unauthorized"}), 401

    doc = Reservation.objects(id=resv_id, user=user).first()
    if not doc:
        return jsonify({"msg": "ไม่พบการจอง"}), 404
    return jsonify(serialize_reservation(doc)), 200

@reservations.route('/reservations/<resv_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_reservation(resv_id):
    user_id = get_jwt_identity()
    user = User.objects(id=user_id).first()
    if not user:
        return jsonify({"msg": "Unauthorized"}), 401

    doc = Reservation.objects(id=resv_id, user=user).first()
    if not doc:
        return jsonify({"msg": "ไม่พบการจอง"}), 404

    data = request.get_json() or {}

    if 'customerName' in data:
        doc.customer_name = (data['customerName'] or '').strip()
    if 'phone' in data:
        doc.phone = (data['phone'] or '').strip()
    if 'partySize' in data:
        doc.party_size = int(data['partySize'])
    if 'status' in data:
        doc.status = data['status']

    if 'reserveStart' in data:
        doc.reserve_start = parse_dt(data['reserveStart'])
    if 'reserveEnd' in data:
        doc.reserve_end = parse_dt(data['reserveEnd'])
    if doc.reserve_start and not doc.reserve_end and data.get('reserveDurationMinutes'):
        doc.reserve_end = doc.reserve_start + timedelta(minutes=int(data['reserveDurationMinutes']))

    # โต๊ะ
    table = None
    if 'tableId' in data and data['tableId']:
        table = Table.objects(id=data['tableId']).first()
    elif 'tableNumber' in data and data['tableNumber']:
        table = Table.objects(number=(data['tableNumber'] or '').strip()).first()
    if table is not None:
        if not table:
            return jsonify({"msg": "ไม่พบโต๊ะ"}), 400
        if not table.is_active:
            return jsonify({"msg": "โต๊ะนี้ถูกปิดใช้งาน"}), 400
        doc.table = table

    # ตรวจคาบเกี่ยว เมื่อสถานะยังใช้งานจริง
    if doc.status in ["reserved", "seated"]:
        if not doc.reserve_start or not doc.reserve_end:
            return jsonify({"msg": "เวลาเริ่ม/สิ้นสุดไม่ถูกต้อง"}), 400
        conflict = Reservation.objects(
            id__ne=doc.id,
            table=doc.table,
            status__in=["reserved", "seated"],
            reserve_start__lt=doc.reserve_end,
            reserve_end__gt=doc.reserve_start
        ).first()
        if conflict:
            return jsonify({"msg": "ช่วงเวลานี้โต๊ะถูกจองแล้ว"}), 409

    try:
        doc.save()
        return jsonify({"msg": "updated", "reservation": serialize_reservation(doc)}), 200
    except Exception as e:
        return jsonify({"msg": f"อัปเดตล้มเหลว: {e}"}), 400

@reservations.route('/reservations/<resv_id>', methods=['DELETE'])
@jwt_required()
def delete_reservation(resv_id):
    user_id = get_jwt_identity()
    user = User.objects(id=user_id).first()
    if not user:
        return jsonify({"msg": "Unauthorized"}), 401

    doc = Reservation.objects(id=resv_id, user=user).first()
    if not doc:
        return jsonify({"msg": "ไม่พบการจอง"}), 404
    doc.delete()
    return jsonify({"msg": "deleted"}), 200

@reservations.route('/reservations/<resv_id>/cancel', methods=['PATCH'])
@jwt_required()
def cancel_reservation(resv_id):
    user_id = get_jwt_identity()
    user = User.objects(id=user_id).first()
    if not user:
        return jsonify({"msg": "Unauthorized"}), 401

    doc = Reservation.objects(id=resv_id, user=user).first()
    if not doc:
        return jsonify({"msg": "ไม่พบการจอง"}), 404
    doc.status = "cancelled"
    doc.save()
    return jsonify({"msg": "cancelled"}), 200

@reservations.route('/reservations/search', methods=['GET'])
@jwt_required()
def search_reservations():
    user_id = get_jwt_identity()
    user = User.objects(id=user_id).first()
    if not user:
        return jsonify({"msg": "Unauthorized"}), 401

    q_name = (request.args.get('customerName') or '').strip()
    q_phone = (request.args.get('phone') or '').strip()
    q_status = (request.args.get('status') or '').strip()
    q_table_number = (request.args.get('tableNumber') or '').strip()

    start_from = parse_dt(request.args.get('startFrom'))
    end_to = parse_dt(request.args.get('endTo'))

    qs = Reservation.objects(user=user)

    if q_name:
        qs = qs.filter(customer_name__icontains=q_name)
    if q_phone:
        qs = qs.filter(phone__icontains=q_phone)
    if q_status:
        qs = qs.filter(status=q_status)
    if q_table_number:
        tables = Table.objects(number__icontains=q_table_number).only('id')
        qs = qs.filter(table__in=[t.id for t in tables])

    if start_from:
        qs = qs.filter(reserve_end__gte=start_from)
    if end_to:
        qs = qs.filter(reserve_start__lte=end_to)

    qs = qs.order_by('-reserve_start')

    if not qs:
        return jsonify({"msg": "No matching reservations found"}), 404

    return jsonify([serialize_reservation(d) for d in qs]), 200
