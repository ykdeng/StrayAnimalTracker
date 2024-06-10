import pytest
from flask import Flask, jsonify, request
from unittest.mock import MagicMock
from app import app as flask_app

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
                return animal
        return None

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def mock_database(monkeypatch):
    mock_db = MockDatabase()
    monkeypatch.setattr('app.db', mock_db, raising=True)
    return mock_db

@pytest.mark.parametrize("animal", [{"id": 1, "name": "Lion", "location": "Africa"}])
def test_create_animal(client, mock_database, animal):
    response = client.post("/animal", json=animal)
    assert response.status_code == 200
    assert mock_database.animals[-1] == animal

def test_read_animal(client, mock_database):
    test_animal = {"id": 1, "name": "Elephant", "location": "Asia"}
    mock_database.create_animal(test_animal)
    response = client.get("/animal/1")
    assert response.status_code == 200
    assert response.json == test_animal

@pytest.mark.parametrize("updated_data", [{"name": "African Lion"}])
def test_update_animal(client, mock_database, updated_data):
    test_animal = {"id": 1, "name": "Lion", "location": "Africa"}
    mock_database.create_animal(test_animal)
    response = client.put("/animal/1", json=updated_data)
    assert response.status_code == 200
    assert mock_database.get_animal(1)['name'] == "African Lion"

def test_delete_animal(client, mock_database):
    test_animal = {"id": 1, "name": "Giraffe", "location": "Africa"}
    mock_database.create_animal(test_animal)
    response = client.delete("/animal/1")
    assert response.status_code == 200
    assert mock_database.get_animal(1) is None