import pytest
from flask import Flask, jsonify, request, make_response
from unittest.mock import MagicMock

app = Flask(__name__)

class MockDatabase:
    def __init__(self):
        self.animals = []

    def create_animal(self, animal):
        self.animals.append(animal)
        return animal

    def get_animal(self, id):
        return next((animal for animal in self.animals if animal['id'] == id), None)

    def update_animal(self, id, animal_data):
        animal = self.get_animal(id)
        if animal:
            animal.update(animal_data)
            return animal
        return None

    def delete_animal(self, id):
        for i, animal in enumerate(self.animals):
            if animal['id'] == id:
                del self.animals[i]
                return True
        return False

db = MockDatabase()

@app.route('/animal', methods=['POST'])
def create_animal():
    animal = request.json
    result = db.create_animal(animal)
    if result:
        return make_response(jsonify(result), 200)
    else:
        return make_response(jsonify({"error": "Animal could not be added"}), 400)

@app.route('/animal/<int:id>', methods=['GET'])
def read_animal(id):
    animal = db.get_animal(id)
    if animal:
        return make_response(jsonify(animal), 200)
    else:
        return make_response(jsonify({"error": "Animal not found"}), 404)

@app.route('/animal/<int:id>', methods=['PUT'])
def update_animal(id):
    animal_data = request.json
    result = db.update_animal(id, animal_data)
    if result:
        return make_result(jsonify(result), 200)
    else:
        return make_response(jsonify({"error": "Animal not found or update failed"}), 404)

@app.route('/animal/<int:id>', methods=['DELETE'])
def delete_animal(id):
    if db.delete_animal(id):
        return make_response(jsonify({"success": "Animal deleted"}), 200)
    else:
        return make_response(jsonify({"error": "Animal not found"}), 404)

@pytest.fixture
def app():
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def mock_database(monkeypatch):
    mock_db = MockDatabase()
    monkeypatch.setattr('app.db', mock_db, raising=True)
    return mock_db

if __name__ == '__main__':
  app.run(debug=True)