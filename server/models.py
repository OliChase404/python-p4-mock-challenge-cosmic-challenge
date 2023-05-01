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
    serialize_only = ('id', 'name', 'distance_from_earth', 'nearest_star', 'image')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.String)
    nearest_star = db.Column(db.String)
    image = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    missions = db.relationship('Mission', backref='planet')
    scientists = association_proxy('missions', 'scientist', creator=lambda sci: Mission(scientist=sci))


class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'
    serialize_only = ('id', 'name', 'field_of_study', 'avatar')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    field_of_study = db.Column(db.String)
    avatar = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    missions = db.relationship('Mission', backref='scientist')
    planets = association_proxy('missions', 'planet', creator=lambda planet: Mission(planet=planet))
    
    @validates('name')
    def validate_name(self, key, name):
        if name:
            return name
        else:
            raise AssertionError('Name cell must not be empty.')

class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'
    serialize_only = ('id', 'name', 'scientist_id', 'planet_id')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    scientist_id = db.Column(db.Integer, db.ForeignKey('scientists.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    @validates('name')
    def validate_name(self, key, name):
        if name:
            return name
        else:
            raise AssertionError('Name cell must not be empty.')
    @validates('scientist_id')
    def validate_scientist_id(self, key, scientist_id):
        if scientist_id:
            return scientist_id
        else:
            raise AssertionError('Scientist ID cell must not be empty.')
    @validates('planet_id')
    def validate_planet_id(self, key, planet_id):
        if planet_id:
            return planet_id
        else:
            raise AssertionError('Planet ID cell must not be empty.')

# add any models you may need. 