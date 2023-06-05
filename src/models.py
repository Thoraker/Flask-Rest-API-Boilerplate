from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
Base = db.declarative_base()


favorite_people = db.Table(
    "favorite_people",
    db.Column("user_id", db.ForeignKey("users.id")),
    db.Column("people_id", db.ForeignKey("peoples.id")),
)


favorite_planet = db.Table(
    "favorite_planet",
    db.Column("user_id", db.ForeignKey("users.id")),
    db.Column("planet_id", db.ForeignKey("planets.id")),
)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=True)
    password = db.Column(db.String(50), unique=True, nullable=True)
    mail = db.Column(db.String(80), unique=True, nullable=True)

    favorite_planets = db.relationship(
        "Planet", secondary=favorite_planet, back_populates="liked"
    )
    favorite_peoples = db.relationship(
        "People", secondary=favorite_people, back_populates="liked"
    )

    def serialize(self):
        return {
            "User name": self.user_name,
            "E-mail": self.mail,
        }


class Planet(db.Model):
    __tablename__ = "planets"
    id = db.Column(db.Integer(), primary_key=True)
    diameter = db.Column(db.String(30), nullable=True)
    rotation_period = db.Column(db.Integer(), nullable=True)
    orbital_period = db.Column(db.Integer(), nullable=True)
    gravity = db.Column(db.String(30), nullable=True)
    population = db.Column(db.Integer(), nullable=True)
    climate = db.Column(db.String(30), nullable=True)
    terrain = db.Column(db.String(30), nullable=True)
    surface_water = db.Column(db.Integer(), nullable=True)
    created = db.Column(db.String(30), nullable=True)
    name = db.Column(db.String(50), unique=True, nullable=True)
    url = db.Column(db.String(50), unique=True, nullable=True)

    liked = db.relationship(
        "User", secondary=favorite_planet, back_populates="favorite_planets"
    )
    natives = db.relationship("People", back_populates="compatriot")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
        }


class People(db.Model):
    __tablename__ = "peoples"
    id = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.Float, nullable=True)
    mass = db.Column(db.Float, nullable=True)
    hair_color = db.Column(db.String(30), nullable=True)
    skin_color = db.Column(db.String(30), nullable=True)
    eye_color = db.Column(db.String(30), nullable=True)
    birth_year = db.Column(db.String(30), nullable=True)
    gender = db.Column(db.String(30), nullable=True)
    created = db.Column(db.String(30), nullable=True)
    name = db.Column(db.String(50), unique=True, nullable=True)
    homeworld = db.Column(db.Integer, db.ForeignKey("planets.id"), nullable=True)
    url = db.Column(db.String(50), unique=True, nullable=True)

    liked = db.relationship(
        "User", secondary=favorite_people, back_populates="favorite_peoples"
    )
    compatriot = db.relationship("Planet", back_populates="natives")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
        }
