# models.py
from mongoengine import Document, StringField, ReferenceField, DateTimeField, IntField, BooleanField
from datetime import datetime

class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)

class Table(Document):
    number = StringField(required=True, unique=True)   # เลขโต๊ะ เช่น A1, 12, VIP-3
    seats = IntField(min_value=1, default=4)           # จำนวนที่นั่ง
    is_active = BooleanField(default=True)             # เปิด/ปิดการใช้งานโต๊ะ

class Reservation(Document):
    customer_name = StringField(required=True)         # ชื่อลูกค้า
    phone = StringField()                              # เบอร์โทร
    party_size = IntField(required=True, min_value=1)  # จำนวนคน

    table = ReferenceField(Table, required=True)       # อ้างอิงโต๊ะที่จอง

    reserve_start = DateTimeField(required=True)       # เวลาเริ่มจอง
    reserve_end = DateTimeField(required=True)         # เวลาสิ้นสุดจอง

    status = StringField(                              
        choices=("reserved", "seated", "completed", "cancelled"),
        default="reserved"
    )

    user = ReferenceField(User)                        # เจ้าของ/ผู้สร้างการจอง

    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
