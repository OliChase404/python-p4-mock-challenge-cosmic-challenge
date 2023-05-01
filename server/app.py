#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from models import Scientist, Planet, Mission, db
from random import choice as rc



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

@app.route('/scientists', methods=['GET', 'POST'])
def scientists():
    if request.method == 'GET':    
        scientists = Scientist.query.all()
        return jsonify([scientist.to_dict() for scientist in scientists])
    
    elif request.method == 'POST':
        new_scientist = Scientist(**request.json)
        db.session.add(new_scientist)
        db.session.commit()
        new_scientist_dict = new_scientist.to_dict()
        response = make_response(jsonify(new_scientist_dict), 201)
        return response

@app.route('/scientists/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def scientist_by_id(id):
    scientist = Scientist.query.get(id)
    if request.method == 'GET':
        return jsonify(scientist.to_dict())
    
    elif request.method == 'PATCH':
        for key, value in request.json.items():
            setattr(scientist, key, value)
        db.session.commit()
        return jsonify(scientist.to_dict())
    
    elif request.method == 'DELETE':
        assigned_missions = db.session.query(Mission).filter(Mission.scientist_id == id).all()
        all_other_scientists = db.session.query(Scientist).filter(Scientist.id != id).all()
        for mission in assigned_missions:
            mission.scientist_id = rc(all_other_scientists).id
            db.session.add(mission)
        db.session.commit()
        db.session.delete(scientist)
        db.session.commit()
        return make_response('', 204)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
    
@app.route('/planets', methods=['GET', 'POST'])
def planets():
    if request.method == 'GET':    
        planets = Planet.query.all()
        return jsonify([planet.to_dict() for planet in planets])
    
    elif request.method == 'POST':
        new_planet = Planet(**request.json)
        db.session.add(new_planet)
        db.session.commit()
        new_planet_dict = new_planet.to_dict()
        response = make_response(jsonify(new_planet_dict), 201)
        return response
    
@app.route('/planets/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def planet_by_id(id):
    planet = Planet.query.get(id)
    if request.method == 'GET':
        return jsonify(planet.to_dict())
    elif request.method == 'PATCH':
        for key, value in request.json.items():
            setattr(planet, key, value)
        db.session.commit()
        return jsonify(planet.to_dict())
    elif request.method == 'DELETE':
        planned_missions = db.session.query(Mission).filter(Mission.planet_id == id).all()
        for mission in planned_missions:
            db.session.delete(mission)
        db.session.delete(planet)
        db.session.commit()
        return make_response('', 204)
    
@app.route('/missions', methods=['GET', 'POST'])
def missions ():
    if request.method == 'GET':    
        missions = Mission.query.all()
        return jsonify([mission.to_dict() for mission in missions])
    
    elif request.method == 'POST':
        new_mission = Mission(**request.json)
        db.session.add(new_mission)
        db.session.commit()
        new_mission_dict = new_mission.to_dict()
        response = make_response(jsonify(new_mission_dict), 201)
        return response
    
@app.route('/missions/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def mission_by_id(id):
    mission = Mission.query.get(id)
    if request.method == 'GET':
        return jsonify(mission.to_dict())
    elif request.method == 'PATCH':
        for key, value in request.json.items():
            setattr(mission, key, value)
        db.session.commit()
        return jsonify(mission.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(mission)
        db.session.commit()
        return make_response('', 204)
