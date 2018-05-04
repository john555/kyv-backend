import uuid
from flask import Flask, request, jsonify, json, make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from .config import app_config

db = SQLAlchemy()

def create_app(config_name):
    from .models import VisitorLog
    app = Flask(__name__)
    api = Api(app)
    app.config.from_object(app_config[config_name])
    db.init_app(app)

    @app.route("/")
    def index():
        return "VMS - Visitor Management System."
    
    class VisitorLogRoutes(Resource):

        def get(self, id=None):
            if id:
                log = VisitorLog.query.filter_by(id=id).first()

                if log:
                    return jsonify(data=log.to_dict())
                else:
                    return make_response(jsonify(error="Resource not found"), 404)
            logs = VisitorLog.query.all()
            return jsonify(
                data=[e.to_dict() for e in logs]
            )

        def post(self):
            data = request.get_json()
            log = VisitorLog()
            log.id = str(uuid.uuid4())

            try:
                log.save_data(data)
            except Exception:
                return make_response(
                    jsonify({
                        "error": "Invalid input"
                    }),
                    409
                )
            return make_response(
                jsonify(
                    data=log.to_dict()
                ),
                201
            )

        def put(self, id):
            log = VisitorLog.query.filter_by(id=id).first()
            body = request.get_json()
            data = {
                 "visitorName": body.get("visitorName", log.visitor_name),
                "hostName": body.get("hostName", log.host_name),
                "purpose": body.get("purpose", log.purpose),
                "cardNumber": body.get("cardNumber", log.card_number)
            }
            log.save_data(data)
            return jsonify(data=log.to_dict())

        def delete(self, id):
            log = VisitorLog.query.filter_by(id=id).first()
            log.delete()
            return jsonify({'id': log.id})
    
    api.add_resource(VisitorLogRoutes,
                    "/api/v1/visitor-logs/",
                    "/api/v1/visitor-logs/<id>")

    return app
