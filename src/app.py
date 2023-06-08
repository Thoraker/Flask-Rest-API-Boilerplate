"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, abort
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


# GET todos los users
@app.route("/user", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200


# POST un nuevo user
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


# GET devuelve "user_id" y sus favoritos
@app.route("/favorite/<string:user_id>", methods=["GET"])
def get_favorite(user_id):
    user = User.query.get(user_id)
    return jsonify(user.serialize2()), 201


# PUT para "user_id" para modificar la data, hacer consulta con formato {"user_name": a, "password": b, "mail": c}
@app.route('/user/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        abort(400)
    user.user_name = request.json['user_name']
    user.password = request.json["password"]
    user.mail = request.json["mail"]
    db.session.commit()
    return jsonify(user.serialize1()), 201


# POST para agregar planet favorito al usuario user_id, hacer consulta con formato { "id": a} donde a es el id del planet favorito
@app.route("/favorite/planet/<string:user_id>", methods=["POST"])
def create_favorite_planet(user_id):
    user = User.query.get(user_id)
    new_favorite = Planet.query.get(request.json['id'])
    user.favorite_planets.append(new_favorite)
    db.session.commit()
    return jsonify(user.serialize2()), 201


# POST para agregar people favorito al usuario user_id, hacer consulta con formato { "id": a} donde a es el id del people favorito
@app.route("/favorite/people/<string:user_id>", methods=["POST"])
def create_favorite_people(user_id):
    user = User.query.get(user_id)
    new_favorite = People.query.get(request.json['id'])
    user.favorite_peoples.append(new_favorite)
    db.session.commit()
    return jsonify(user.serialize2()), 201


# GET todos los people
@app.route("/people", methods=["GET"])
def get_peoples():
    peoples = People.query.all()
    return jsonify([people.serialize() for people in peoples]), 200


# POST un nuevo people
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
        name=request.json["name"],
        homeworld=request.json["homeworld"],
    )
    db.session.add(newPeople)
    db.session.commit()
    return jsonify(newPeople.serialize()), 201

# GET people segun id indicado
@app.route("/people/<string:id>", methods=["GET"])
def get_people(id):
    people = People.query.get(id)
    if people is None:
        abort(404)
    return jsonify(people.serialize2())


# GET todos los planet
@app.route("/planet", methods=["GET"])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize1() for planet in planets]), 200


# POST un nuevo planet
@app.route("/planet", methods=["POST"])
def create_planet():
    newPlanet = Planet(
        diameter=request.json["diameter"],
        rotation_period=request.json["rotation_period"],
        orbital_period=request.json["orbital_period"],
        gravity=request.json["gravity"],
        population=request.json["population"],
        climate=request.json["climate"],
        terrain=request.json["terrain"],
        surface_water=request.json["surface_water"],
        name=request.json["name"],
    )
    db.session.add(newPlanet)
    db.session.commit()
    return jsonify(newPlanet.serialize()), 201


# GET planet segun id indicado
@app.route("/planet/<string:id>", methods=["GET"])
def get_planet(id):
    planet = People.query.get(id)
    if planet is None:
        abort(404)
    return jsonify(planet.serialize2())


#DELETE planet favorito al usuario user_id 
@app.route("/favorite/planet/<string:user_id>", methods=['DELETE'])
def delete_favorite_planet(user_id):
    user = User.query.get(user_id)
    unfavorite = Planet.query.get(request.json['id'])
    user.favorite_planets.remove(unfavorite)
    db.session.commit()
    return jsonify(user.serialize2()), 201


#DELETE people favorito al usuario user_id
@app.route("/favorite/people/<string:user_id>", methods=['DELETE'])
def delete_favorite_people(user_id):
    user = User.query.get(user_id)
    unfavorite = People.query.get(request.json['id'])
    user.favorite_planets.remove(unfavorite)
    db.session.commit()
    return jsonify(user.serialize2()), 201


# this only runs if `$ python src/app.py` is executed
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT, debug=False)
