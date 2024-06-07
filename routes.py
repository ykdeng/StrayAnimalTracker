from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class AnimalSighting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    date_spotted = db.Column(db.DateTime, nullable=False)

    def __init__(self, animal_name, location, date_spotted):
        self.animal_name = animal_name
        self.location = location
        self.date_spotted = date_spotted

    def to_dict(self):
        return {
            'id': self.id,
            'animal_name': self.animal_name,
            'location': self.location,
            'date_spotted': self.date_spotted.isoformat()
        }

@app.route('/animal_sighting', methods=['POST'])
def add_animal_sighting():
    data = request.get_json()
    new_sighting = AnimalSighting(animal_name=data['animal_name'], location=data['location'], date_spotted=data['date_spotted'])
    db.session.add(new_sighting)
    db.session.commit()
    return jsonify(new_sighting.to_dict()), 201

@app.route('/animal_sightings', methods=['GET'])
def get_animal_sightings():
    sightings = AnimalSighting.query.all()
    return jsonify([s.to_dict() for s in sightings])

@app.route('/animal_sighting/<int:id>', methods=['GET'])
def get_animal_sighting(id):
    sighting = AnimalSighting.query.get_or_404(id)
    return jsonify(sighting.to_dict())

@app.route('/animal_sighting/<int:id>', methods=['PUT'])
def update_animal_sighting(id):
    sighting = AnimalSighting.query.get_or_404(id)
    data = request.get_json()
    sighting.animal_name = data['animal_name']
    sighting.location = data['location']
    sighting.date_spotted = data['date_spotted']
    db.session.commit()
    return jsonify(sighting.to_dict())

@app.route('/animal_sighting/<int:id>', methods=['DELETE'])
def delete_animal_sighting(id):
    sighting = AnimalSighting.query.get_or_404(id)
    db.session.delete(sighting)
    db.session.commit()
    return jsonify({'message': 'Successfully deleted'})

if __name__ == '__main__':
    app.run(debug=True)