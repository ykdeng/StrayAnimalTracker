import pytest
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base, Animal
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("TEST_DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
        Base.metadata.drop_all(bind=engine)

def test_create_animal(db_session):
    try:
        new_animal = Animal(name="Lion", habitat="Savannah")
        db_session.add(new_animal)
        db_session.commit()
        saved_animal = db_sort.query(Ani).filter_by(name="Lion").first()
        assert saved_animal is not None
        assert saved_animal.name == "Lion"
        assert saved_animal.habitat == "Savannah"
    except exc.SQLAlchemyError as e:
        db_session.rollback()
        pytest.fail(f"SQLAlchemyError during test_create_animal: {e}")

def test_read_animal(db_session):
    try:
        animal = db_session.query(Animal).filter_by(name="Lion").first()
        assert animal is not None
        assert animal.name == "Lion"
    except exc.SQLAlchemyError as e:
        pytest.fail(f"SQLAlchemyError during test_read_animal: {e}")

def test_update_animal(db_session):
    try:
        animal_to_update = db_session.query(Animal).filter_by(name="Lion").first()
        animal_to_update.habitat = "Zoo"
        db_session.commit()
        updated_animal = db_session.query(Animal).filter_by(name="Lion").first()
        assert updated_animal.habitat == "Zoo"
    except exc.SQLAlchemyError as e:
        db_session.rollback()
        pytest.fail(f"SQLAlchemyError during test_update_animal: {e}")

def test_delete_anal(db_session):
    try:
        animal_to_delete = db_session.query(Animal).filter_by(name="Lion").first()
        db_session.delete(animal_to_delete)
        db_session.commit()
        deleted_animal = db_session.query(Animal).filter_by(name="Lion").first()
        assert deleted_animal is None
    except exc.SQLAlchemyError as e:
        db_session.rollback()
        pytest.fail(f"SQLAlchemyError during test_delete_animal: {e}")