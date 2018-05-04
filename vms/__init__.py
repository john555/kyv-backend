import uuid
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from .config import app_config

db = SQLAlchemy()

def create_app(config_name):
    from .models import VisitorLog
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    db.init_app(app)

    @app.route("/")
    def index():
        return "Hello, world"

    @app.route("/api/v1/visitor-logs/", methods=["GET", "POST"])
    def create_visitor_log():
        if request.method == "POST":
            data = request.get_json()
            log = VisitorLog()
            log.id = str(uuid.uuid4())
            log.visitor_name = data.get("visitorName")
            log.host_name = data.get("hostName")
            log.purpose = data.get("purpose")
            log.card_number = data.get("cardNumber")

            try:
                log.save()
            except Exception as e:
                print(e)
                return jsonify({
                    "error": "Invalid data"
                }), 409
            return jsonify(log.to_dict()), 201
        else:
            logs = VisitorLog.query.all()
            return jsonify([e.to_dict() for e in logs])
    return app
