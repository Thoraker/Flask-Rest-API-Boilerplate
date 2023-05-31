from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base

db = SQLAlchemy()
Base = declarative_base()


favorites = db.Table(
    "favorites",
    db.Column("user_id", db.ForeignKey("users.id"), primary_key=True),
    db.Column("element_id", db.ForeignKey("elements.id"), unique=True, nullable=True),
)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(80), unique=False, nullable=True)

    elements = db.relationship("Element", secondary="favorites", back_populates="users")

    def __repr__(self):
        return "<User %r>" % self.name

    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
        }


class Element(db.Model):
    __tablename__ = "elements"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=True)
    details = db.Column(db.String(250), nullable=True)
    section_id = db.Column(db.Integer, db.ForeignKey("sections.id"))

    users = db.relationship("User", secondary="favorites", back_populates="elements")

    def __repr__(self):
        return "<Element %r>" % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "details": self.details,
            "section": self.section_id,
        }


class Section(db.Model):
    __tablename__ = "sections"
    id = db.Column(db.Integer, primary_key=True)
    section_name = db.Column(db.String(50), unique=True, nullable=True)

    def __repr__(self):
        return "<Section %r>" % self.section_name

    def serialize(self):
        return {"id": self.id, "name": self.section_name}
