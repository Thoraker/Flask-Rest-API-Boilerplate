"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Element, Section

# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url.replace(
        "postgres://", "postgresql://"
    )
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# generate sitemap with all your endpoints
@app.route("/")
def sitemap():
    return generate_sitemap(app)


@app.route("/user", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200


@app.route("/user", methods=["POST"])
def add_user():
    name = request.json["name"]
    email = request.json["email"]
    password = request.json["password"]
    new_user = User(name, email, password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201


@app.route("/people", methods=["GET"])
def get_peoples():
    peoples = Element.query.get()
    return jsonify([people.serialize() for people in peoples]), 200


@app.route("/planet", methods=["GET"])
def get_planets():
    planets = Element.query.get()
    return jsonify([planet.serialize() for planet in planets]), 200


@app.route("/section", methods=["POST"])
def add_section():
    new_section = Section(
        name=request.json["name"],
    )
    db.session.add(new_section)
    db.session.commit()
    return jsonify(new_section.serialize()), 201


# this only runs if `$ python src/app.py` is executed
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT, debug=False)
