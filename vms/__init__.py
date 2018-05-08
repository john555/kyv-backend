import uuid, base64
from functools import wraps
from flask import Flask, request, jsonify, json, make_response, current_app
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from jose import jwt
from .config import app_config
from .validation import is_empty

db = SQLAlchemy()

def create_app(config_name):
    from .models import VisitorLog
    app = Flask(__name__)
    api = Api(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config.from_object(app_config[config_name])
    db.init_app(app)

    def authenticate(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            authorization_header = request.headers.get('Authorization')
            if not authorization_header:
                return make_response(jsonify(error="The authorization header is missing."), 403)
            _token = str(authorization_header).split(" ")
            token = _token[1] if len(_token) > 1 else _token[0]

            if not token:
                return make_response(jsonify(error="The authorization header is missing."), 403)
            
            try:
                key = base64.b64decode(current_app.config.get("SECRET")).decode("UTF-8")
            except Exception as e:
                print('Invalid secret key')

            try:
                data = jwt.decode(token, key, algorithms=["RS256"], options={"verify_signature": False})
            except Exception:
                return make_response(jsonify(error="Invalid token."), 403)
                
            return f(*args, **kwargs)
        return decorated

    @app.route("/")
    def index():
        return "VMS - Visitor Management System."
    
    class VisitorLogRoutes(Resource):

        @authenticate
        def get(self, id=None):
            if id:
                log = VisitorLog.query.filter_by(id=id).first()

                if log:
                    return jsonify(data=log.to_dict())
                else:
                    return make_response(jsonify(error="Resource not found."), 404)
            logs = VisitorLog.query.all()
            return jsonify(
                data=[e.to_dict() for e in logs]
            )

        @authenticate
        def post(self, id=None):
            if id:
                return make_response(jsonify(error="Resource not found."), 404)
                
            data = request.get_json()
            
            log = VisitorLog()
            log.id = str(uuid.uuid4())

            if is_empty(data.get("visitorName")):
                return make_response(
                    jsonify({
                        "error": "The visitor's name is required."
                    }),
                    409
                )

            if is_empty(data.get("hostName")):
                return make_response(
                    jsonify({
                        "error": "The host's name is required."
                    }),
                    409
                )
            
            if is_empty(data.get("purpose")):
                return make_response(
                    jsonify({
                        "error": "The visitor's purpose of visit is required."
                    }),
                    409
                )

            if is_empty(data.get("cardNumber")):
                return make_response(
                    jsonify({
                        "error": "The visitor's card number is required."
                    }),
                    409
                )
            
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

        @authenticate
        def put(self, id=None):
            if not id:
                return make_response(jsonify(error="Resource not found."), 404)

            log = VisitorLog.query.filter_by(id=id).first()

            if not log:
                return make_response(jsonify(error="Resource not found."), 404)

            visitor_name = log.visitor_name
            host_name = log.host_name
            purpose = log.purpose
            card_number = log.card_number
            body = request.get_json()

            if not is_empty(body.get("visitorName")):
                visitor_name = body.get("visitorName")
            
            if not is_empty(body.get("hostName")):
                host_name = body.get("hostName")
            
            if not is_empty(body.get("purpose")):
                purpose = body.get("purpose")
            
            if not is_empty(body.get("cardNumber")):
                card_number = body.get("cardNumber")

            data = {
                 "visitorName": visitor_name,
                "hostName": host_name,
                "purpose": log.purpose,
                "cardNumber": log.card_number
            }
            log.save_data(data)
            return jsonify(data=log.to_dict())

        @authenticate
        def delete(self, id=None):
            if not id:
                return make_response(jsonify(error="Resource not found."), 404)

            log = VisitorLog.query.filter_by(id=id).first()

            if not log:
                return make_response(jsonify(error="Resource not found."), 404)
                
            log.delete()
            return jsonify({'id': log.id})
    
    api.add_resource(VisitorLogRoutes,
                    "/api/v1/visitor-logs",
                    "/api/v1/visitor-logs/",
                    "/api/v1/visitor-logs/<id>")

    return app
