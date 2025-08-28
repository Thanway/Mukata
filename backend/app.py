from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from mongoengine import connect
from config import Config

from routes.auth import auth
from routes.tables import tables
from routes.reservations import reservations

app = Flask(__name__)
app.config.from_object(Config)

# CORS: อนุญาต frontend ที่ :3000 และเปิดให้ใช้ METHODS/HEADERS ตามที่ต้องการ
CORS(
    app,
    resources={r"/api/*": {"origins": "*"}},
    supports_credentials=True,
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# JWT
JWTManager(app)

# MongoEngine connect
connect(
    db=app.config["MONGODB_SETTINGS"]["db"],
    host=app.config["MONGODB_SETTINGS"]["host"],
    alias="default",
)

# Blueprints
app.register_blueprint(auth, url_prefix="/api")
app.register_blueprint(tables, url_prefix="/api")
app.register_blueprint(reservations, url_prefix="/api")

# (ทางเลือก) health check
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    # debug=True เพื่อดู stacktrace เวลาเกิด 500
    app.run(host="0.0.0.0", port=5000, debug=True)
