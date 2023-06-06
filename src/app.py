"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, abort
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet

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


# Rutas de User


@app.route("/user", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200


@app.route("/user", methods=["POST"])
def create_user():
    newUser = User(
        user_name=request.json["user_name"],
        password=request.json["password"],
        mail=request.json["mail"],
    )
    db.session.add(newUser)
    db.session.commit()
    return jsonify(newUser.serialize()), 201


@app.route("/user/favorite/<string:user_id>", methods=["GET"])
def get_favorite(user_id):
    user = User.query.get(user_id)
    print(user.__dict__)
    return jsonify(user.serialize1()), 201


# Rutas de People


@app.route("/people", methods=["GET"])
def get_peoples():
    peoples = People.query.all()
    return jsonify([people.serialize() for people in peoples]), 200


@app.route("/people", methods=["POST"])
def create_people():
    newPeople = People(
        height=request.json["height"],
        mass=request.json["mass"],
        hair_color=request.json["hair_color"],
        skin_color=request.json["skin_color"],
        eye_color=request.json["eye_color"],
        birth_year=request.json["birth_year"],
        gender=request.json["gender"],
        created=request.json["created"],
        name=request.json["name"],
        homeworld=request.json["homeworld"],
        url=request.json["url"],
    )
    db.session.add(newPeople)
    db.session.commit()
    return jsonify(newPeople.serialize()), 201


@app.route("/people/<string:item_id>", methods=["GET"])
def get_people(item_id):
    people = People.query.get(item_id)
    if people is None:
        abort(404)
    return jsonify(people.serialize2())


# Rutas de Planet


@app.route("/planet", methods=["GET"])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200


@app.route("/planet/<string:item_id>", methods=["GET"])
def get_planet(item_id):
    planet = People.query.get(item_id)
    if planet is None:
        abort(404)
    return jsonify(planet.serialize2())


# this only runs if `$ python src/app.py` is executed
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT, debug=False)
