from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'stray_animals.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    reported_at = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, species, location):
        self.species = species
        self.location = location

class AnimalSchema(ma.Schema):
    class Meta:
        fields = ('id', 'species', 'location', 'reported_at')

animal_schema = AnimalSchema()
animals_schema = AnimalSchema(many=True)

@app.route('/animal', methods=['POST'])
def add_animal():
    species = request.json['species']
    location = request.json['location']

    new_animal = Animal(species, location)

    db.session.add(new_animal)
    db.session.commit()

    return animal_schema.jsonify(new_animal)

@app.route('/animal', methods=['GET'])
def get_animals():
    all_animals = Animal.query.all()
    result = animals_schema.dump(all_animals)
    return jsonify(result)

@app.route('/animal/<id>', methods=['GET'])
def get_animal(id):
    animal = Animal.query.get(id)
    return animal_schema.jsonify(animal)

@app.route('/animal/<id>', methods=['PUT'])
def update_animal(id):
    animal = Animal.query.get(id)

    species = request.json['species']
    location = request.json['location']

    animal.species = species
    animal.location = location

    db.session.commit()

    return animal_schema.jsonify(animal)

@app.route('/animal/<id>', methods=['DELETE'])
def delete_animal(id):
    animal = Animal.query.get(id)
    db.session.delete(animal)
    db.session.commit()

    return animal_schema.jsonify(animal)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)