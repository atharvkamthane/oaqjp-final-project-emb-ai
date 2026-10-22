"""Flask application for the DevOps Capstone Accounts REST API."""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_talisman import Talisman


def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.update({"TESTING": False, "ACCOUNTS": {}, "NEXT_ACCOUNT_ID": 1, "FORCE_HTTPS": False})
    if test_config:
        app.config.update(test_config)
    CORS(app, resources={r"/*": {"origins": "*"}})
    Talisman(app, force_https=app.config["FORCE_HTTPS"], strict_transport_security=app.config["FORCE_HTTPS"], content_security_policy={"default-src": ["'self'"], "object-src": ["'none'"], "frame-ancestors": ["'none'"]}, session_cookie_secure=app.config["FORCE_HTTPS"], session_cookie_http_only=True, session_cookie_samesite="Lax")

    @app.get("/")
    def index():
        return jsonify(name="Account REST API Service", version="1.0")

    @app.post("/accounts")
    def create_account():
        payload = request.get_json(silent=True) or {}
        if not payload.get("name") or not payload.get("email"):
            return jsonify(error="Both name and email are required"), 400
        account_id = str(app.config["NEXT_ACCOUNT_ID"])
        app.config["NEXT_ACCOUNT_ID"] += 1
        account = {"id": account_id, "name": payload["name"], "email": payload["email"]}
        app.config["ACCOUNTS"][account_id] = account
        return jsonify(account), 201

    @app.get("/accounts")
    def list_accounts():
        return jsonify(list(app.config["ACCOUNTS"].values())), 200

    @app.get("/accounts/<account_id>")
    def read_account(account_id):
        account = app.config["ACCOUNTS"].get(account_id)
        return (jsonify(account), 200) if account else (jsonify(error="Account not found"), 404)

    @app.put("/accounts/<account_id>")
    def update_account(account_id):
        account = app.config["ACCOUNTS"].get(account_id)
        if account is None:
            return jsonify(error="Account not found"), 404
        payload = request.get_json(silent=True) or {}
        for field in ("name", "email"):
            if field in payload:
                account[field] = payload[field]
        return jsonify(account), 200

    @app.delete("/accounts")
    def delete_account_collection():
        payload = request.get_json(silent=True) or {}
        account_id = str(payload.get("id", ""))
        if not account_id or account_id not in app.config["ACCOUNTS"]:
            return jsonify(error="Account not found"), 404
        del app.config["ACCOUNTS"][account_id]
        return "", 204

    @app.delete("/accounts/<account_id>")
    def delete_account(account_id):
        if account_id not in app.config["ACCOUNTS"]:
            return jsonify(error="Account not found"), 404
        del app.config["ACCOUNTS"][account_id]
        return "", 204

    return app


app = create_app()
