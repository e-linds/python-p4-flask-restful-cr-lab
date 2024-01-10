#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        all_plants_dict = []
        for each in plants:
            all_plants_dict.append(each.to_dict())
        return all_plants_dict, 200

    def post(self):
        json_dict = request.get_json()
        new_plant = Plant(
            name = json_dict.get("name"),
            image = json_dict.get("image"),
            price = json_dict.get("price")
        )
        db.session.add(new_plant)
        db.session.commit()
        return new_plant.to_dict(), 200
    

api.add_resource(Plants, '/plants')


class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter(Plant.id == id).first()
        return plant.to_dict(), 200

    def patch(self, id):
        plant = Plant.query.filter(Plant.id == id).first()
        json_dict = request.get_json()
        for attr in json_dict:
            setattr(plant, attr, json_dict.get(attr))
        db.session.add(plant)
        db.session.commit()
        return plant.to_dict(), 200


    def delete(self, id):
        plant = Plant.query.filter(Plant.id == id).first()
        db.session.delete(plant)
        db.session.commit()
        return {"Status": "Deleted"}, 200


api.add_resource(PlantByID, '/plants/<int:id>')

        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
