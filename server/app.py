#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return ''

@app.route('/scientists', methods = ['GET', 'POST'])
def get_scientists():
    scientists = Scientist.query.all()
    if request.method == 'GET':
        return make_response([scientist.to_dict(only=('id', 'name', 'field_of_study')) for scientist in scientists], 200)
    elif request.method == 'POST':
        data = request.get_json()
        try:
            new_scientist = Scientist(
                name = data['name'],
                field_of_study = data['field_of_study']
            )
            db.session.add(new_scientist)
            db.session.commit()
        except Exception as e:
            return make_response({"errors": ["validation errors"]}, 400)
        return make_response(new_scientist.to_dict(), 201)
    
@app.route('/scientists/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
def scientists_by_id(id):
    scientist = Scientist.query.filter(Scientist.id == id).first()
    if not scientist:
            return make_response({"error": "Scientist not found"}, 404)
    elif request.method == 'GET':
        return make_response(scientist.to_dict(), 200)
    elif request.method == 'PATCH':
        data = request.get_json()
        try:
            for attr in data:
                setattr(scientist, attr, data[attr])
            db.session.add(scientist)
            db.session.commit()
        except Exception as e:
            return make_response({"errors": ["validation errors"]}, 400)
        return make_response(scientist.to_dict(only=('id', 'name', 'field_of_study')), 202)
    elif request.method == 'DELETE':
        db.session.delete(scientist)
        db.session.commit()
        return {}, 204
    
@app.route('/planets')
def get_planets():
    return make_response([planet.to_dict(only=('id', 'name', 'distance_from_earth', 'nearest_star')) for planet in Planet.query.all()], 200)

@app.route('/missions', methods = ['POST'])
def new_mission():
    data = request.get_json()
    if request.method == 'POST':
        try:
            new_mission = Mission(
                name = data['name'],
                scientist_id = data['scientist_id'],
                planet_id = data['planet_id']
            )
            db.session.add(new_mission)
            db.session.commit()
        except Exception as e:
            return make_response({"errors": ["validation errors"]}, 400)
        return make_response(new_mission.to_dict(), 201)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
