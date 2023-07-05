# models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


db = SQLAlchemy()


class Hero(db.Model, SerializerMixin):
    __tablename__ = "heroes"
    serialize_rules = ("-powers.heroes",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    # power_id = Column(Integer, ForeignKey("powers.id"))

    powers = db.relationship("HeroPower", backref="heroe")

    def __repr__(self):
        return f"Hero {self.name} has {self.super_name}."


class Power(db.Model, SerializerMixin):
    __tablename__ = "powers"
    serialize_rules = ("-heroes.powers",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    heroes = db.relationship("HeroPower", backref="power")

    def __repr__(self):
        return f"Power {self.name} to {self.description}."

    @validates("description")
    def validate_description(self, key, description):
        if description and len(description) < 20:
            raise ValueError("Description must be atleast 20 characters long.")
        return description


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = "hero_powers"
    serialize_rules = ("-heroes.powers", "-powers.heroes")

    id = db.Column(db.Integer, primary_key=True)
    strength =db.Column(db.String)
    hero_id = db.Column(db.Integer, db.ForeignKey("heroes.id"))
    power_id = db.Column(db.Integer, db.ForeignKey("powers.id"))

    # hero = db.relationship(
    #     "Hero", backref=db.backref("hero_powers", cascade="all, delete-orphan")
    # )
    # power = db.relationship(
    #     "Power", backref=db.backref("hero_powers", cascade="all, delete-orphan")
    # )

    def __repr__(self):
        return f"HeroPower: hero_id={self.hero_id}, power_id={self.power_id}"

    @validates("strength")
    def validate_strength(self, key, strength):
        valid_strengths = ["Strong", "Weak", "Average"]
        if strength not in valid_strengths:
            raise ValueError(
                f"Invalid strength. Allowed values: {', '.join(valid_strengths)}"
            )
        return strength