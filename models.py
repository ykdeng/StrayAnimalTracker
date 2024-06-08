from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from dotenv import load_dotenv

load_dotenv()
Base = declarative_base()

class Animal(Base):
    __tablename__ = 'animals'
    id = Column(Integer, primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    photo_url = Column(String, nullable=True)

    def __repr__(self):
        return f"<Animal(id='{self.id}', latitude='{self.latitude}', longitude='{self.longitude}', description='{self.description}', photo_url='{self.photo_url}')>"

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///default.db')

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker(bind=engine))

def add_animals(animals_data):
    """
    animals_data: A list of dictionaries where each dictionary contains data for one animal.
    Example: [{'latitude': 34.0522, 'longitude': -118.2437, 'description': 'desc', 'photo_url': 'url'}, {...}]
    """
    session = Session()
    animals = [Animal(**data) for data in animals_data]
    session.add_all(animals)
    session.commit()
    for animal in animals:
        print(f"Added new animal with ID: {animal.id}")
    session.close()

if __name__ == "__main__":
    animals_to_add = [
        {'latitude': 34.0522, 'longitude': -118.2437, 'description': 'Small brown dog with no collar', 'photo_url': 'http://example.com/photo1.jpg'},
    ]
    add_animals(animals_to_add)