from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.Integer)
    nearest_star = db.Column(db.String)

    # Add relationship
    mission = db.relationship('Mission', back_populates='planet', cascade="all, delete")
    # Add serialization rules
    serialize_rules = ('-mission.planet',)

class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)

    # Add relationship
    mission = db.relationship('Mission', back_populates='scientist', cascade="all, delete")
    # Add serialization rules
    serialize_rules = ('-mission.scientist',)
    # Add validation
    @validates('name')
    def validates_name(self, key, value):
        if not value:
            raise ValueError("Not name")
        return value
    
    @validates('field_of_study')
    def validates_field(self, key, value):
        if not value:
            raise ValueError("No field of study")
        return value

class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    scientist_id = db.Column(db.Integer, db.ForeignKey('scientists.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    # Add relationships
    scientist = db.relationship('Scientist', back_populates='mission')
    planet = db.relationship('Planet', back_populates='mission')
    # Add serialization rules
    serialize_rules = ('-scientist.mission', '-planet.mission',)
    # Add validation
    @validates('name')
    def validates_name(self, key, value):
        if not value:
            raise ValueError("Not name")
        return value
    
    @validates('scientist_id')
    def validates_sid(self, key, value):
        if not value:
            raise ValueError("No scientist ID")
        return value
    
    @validates('planet_id')
    def validates_pid(self, key, value):
        if not value:
            raise ValueError("No planet ID")
        return value

# add any models you may need.
