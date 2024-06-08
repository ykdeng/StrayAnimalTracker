from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Ensure this directory exists
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

db = SQLAlchemy(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class AnimalSighting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    date_spotted = db.Column(db.DateTime, nullable=False)
    photo_filename = db.Column(db.String(120))

    def __init__(self, animal_name, location, date_spotted, photo_filename=None):
        self.animal_name = animal_name
        self.location = location
        self.date_spotted = date_spotted
        self.photo_filename = photo_filename

    def to_dict(self):
        return {
            'id': self.id,
            'animal_name': self.animal_name,
            'location': self.location,
            'date_spotted': self.date_spotted.isoformat(),
            'photo_url': request.host_url + 'uploads/' + self.photo_filename if self.photo_filename else None
        }

@app.route('/animal_sighting', methods=['POST'])
def add_animal_sighting():
    data = request.form
    file = request.files.get('photo')
    filename = None
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
    new_sighting = AnimalSighting(
        animal_name=data.get('animal_name'), 
        location=data.get('location'), 
        date_spotted=data.get('date_spotted'),
        photo_filename=filename
        )
    db.session.add(new_sighting)
    db.session.commit()
    return jsonify(new_sighting.to_dict()), 201

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/animal_sightings', methods=['GET'])
def get_animal_sightings():
    sightings = AnimalSighting.query.all()
    return jsonify([s.to_dict() for s in sightings])

@app.route('/animal_sighting/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_animal_sighting(id):
    if request.method == 'GET':
        sighting = AnimalSighting.query.get_or_404(id)
        return jsonify(sighting.to_dict())
    elif request.method == 'PUT':
        sighting = AnimalSighting.query.get_or_404(id)
        data = request.form
        sighting.animal_name = data.get('animal_name')
        sighting.location = data.get('location')
        sighting.date_spotted = data.get('date_spotted')
        file = request.files.get('photo')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            sighting.photo_filename = filename  # Update only if a new file uploaded
        db.session.commit()
        return jsonify(sighting.to_dict())
    elif request.method == 'DELETE':
        sighting = AnimalSighting.query.get_or_404(id)
        db.session.delete(sighting)
        db.session.commit()
        return jsonify({'message': 'Successfully deleted'})

if __name__ == '__main__':
    app.run(debug=True)