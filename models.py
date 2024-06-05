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

# Function to add a new animal
def add_animal(latitude, longitude, description=None, photo_url=None):
    session = Session()
    new_animal = Animal(latitude=latitude, longitude=longitude, description=description, photo_url=photo_url)
    session.add(new_animal)
    session.commit()
    print(f"Added new animal with ID: {new_animal.id}")
    session.close()

# Function to query animals, optionally by description
def query_animals(description=None):
    session = Session()
    if description:
        animals = session.query(Animal).filter(Animal.description.like(f"%{description}%")).all()
    else:
        animals = session.query(Animal).all()
    session.close()
    return animals

# Example Usage
if __name__ == "__main__":
    add_animal(34.0522, -118.2437, "Small brown dog with no collar", "http://example.com/photo1.jpg")
    animals = query_animals("brown dog")
    for animal in animals:
        print(animal)
