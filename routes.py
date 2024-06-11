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

def is_file_extension_allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class Sighting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_type = db.Column(db.String(120), nullable=False)
    spotted_location = db.Column(db.String(120), nullable=False)
    spotted_date = db.Column(db.DateTime, nullable=False)
    image_filename = db.Column(db.String(120))

    def __init__(self, animal_type, spotted_location, spotted_date, image_filename=None):
        self.animal_type = animal_type
        self.spotted_location = spotted_location
        self.spotted_date = spotted_date
        self.image_filename = image_filename

    def to_json(self):
        return {
            'id': self.id,
            'animal_type': self.animal_type,
            'spotted_location': self.spotted_location,
            'spotted_date': self.spotted_date.isoformat(),
            'image_url': request.host_url + 'uploads/' + self.image_filename if self.image_filename else None
        }

@app.route('/save_sighting', methods=['POST'])
def save_sighting():
    sighting_details = request.form
    image_file = request.files.get('image')
    image_name = None
    if image_file and is_file_extension_allowed(image_file.filename):
        image_name = secure_filename(image_file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
        image_file.save(image_path)
    new_sighting_record = Sighting(
        animal_type=sighting_details.get('animal_type'), 
        spotted_location=sighting_details.get('spotted_location'), 
        spotted_date=sighting_details.get('spotted_date'),
        image_filename=image_name
        )
    db.session.add(new_sighting_record)
    db.session.commit()
    return jsonify(new_sighting_record.to_json()), 201

@app.route('/image/<filename>')
def serve_uploaded_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/sightings', methods=['GET'])
def list_sightings():
    all_sightings = Sighting.query.all()
    return jsonify([sighting.to_json() for sighting in all_sightings])

@app.route('/sighting/<int:sighting_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_sighting(sighting_id):
    if request.method == 'GET':
        sighting_record = Sighting.query.get_or_404(sighting_id)
        return jsonify(sighting_record.to_json())
    elif request.method == 'PUT':
        sighting_record = Sighting.query.get_or_404(sighting_id)
        update_data = request.form
        sighting_record.animal_type = update_data.get('animal_type')
        sighting_record.spotted_location = update_data.get('spotted_location')
        sighting_record.spotted_date = update_data.get('spotted_date')
        image_file = request.files.get('image')
        if image_file and is_file_extension_allowed(image_file.filename):
            image_name = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
            image_file.save(image_path)
            sighting_record.image_filename = image_name  # Update only if a new file is uploaded
        db.session.commit()
        return jsonify(sighting_record.to_json())
    elif request.method == 'DELETE':
        sighting_record = Sighting.query.get_or_404(sighting_id)
        db.session.delete(sighting_record)
        db.session.commit()
        return jsonify({'message': 'Sighting successfully deleted'})

if __name__ == '__main__':
    app.run(debug=True)