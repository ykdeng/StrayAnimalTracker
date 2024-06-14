import pytest
from flask import Flask, jsonify, request
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

def make_api_response(data, status_code=200, error_message=None):
    if error_message:
        data = {"error": error_message}
    return jsonify(data), status_code

@app.route('/animal', methods=['POST'])
def create_animal():
    animal = request.json
    result = db.create_animal(animal)
    return make_api_response(result) if result else make_api_response({}, 400, "Animal could not be added")

@app.route('/animal/<int:id>', methods=['GET'])
def read_animal(id):
    animal = db.get_animal(id)
    return make_api_response(animal) if animal else make_api_response({}, 404, "Animal not found")

@app.route('/animal/<int:id>', methods=['PUT'])
def update_animal(id):
    animal_data = request.json
    result = db.update_animal(id, animal_data)
    return make_api_response(result) if result else make_api_response({}, 404, "Animal not found or update failed")

@app.route('/animal/<int:id>', methods=['DELETE'])
def delete_animal(id):
    return make_api_response({"success": "Animal deleted"}) if db.delete_animal(id) else make_api_response({}, 404, "Animal not found")

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