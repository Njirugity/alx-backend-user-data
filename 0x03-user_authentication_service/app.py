#!/usr/bin/env python3
from flask import Flask, jsonify,request, make_response
from auth import Auth

auth = Auth()
app = Flask(__name__)

@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """
    Return json respomse
    {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"})

@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        return make_response(jsonify({"message": "Email and password are required"}), 400)
    try:
        new_user = auth.register_user(email, password)
        
    except ValueError as e:
        return make_response(jsonify({"message": "email already registered"}), 400)
    return jsonify({"email":email,"message":"user created"})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
