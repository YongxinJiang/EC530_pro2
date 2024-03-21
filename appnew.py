import os
import logging
from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from celery import Celery

from flask import Flask, request, jsonify
import celery
import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Flatten
from PIL import Image
import io
app = Flask(__name__)

log_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.log')
logging.basicConfig(filename=log_file, level=logging.INFO)

api = Api(app)

database_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')

# Configure the application to use SQLite as the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

class ImageClassification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    classification = db.Column(db.String(50), nullable=False)

    def __init__(self, filename, classification):
        self.filename = filename
        self.classification = classification

image_definition = {
    'id': fields.Integer,
    'filename': fields.String,
    'classification': fields.String
}

parser = reqparse.RequestParser()
parser.add_argument('filename', help="Filename cannot be blank")
parser.add_argument('classification', help="Classification cannot be blank")

def get_image(image_id):
    with app.app_context():
        image = ImageClassification.query.filter_by(id=image_id).first()
        try:
            if image:
                return {'id': image.id, 'filename': image.filename, 'classification': image.classification}
            else:
                return {'error': 'No such image found'}, 404
        except Exception as e:
            logging.error(f"Error getting image: {e}")
            print(e)

# Celery task for inference processing
@celery.task
def train_model_async():
    model = Sequential([
        Flatten(input_shape=(28, 28)),
        Dense(128, activation='relu'),
        Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    train_images = np.random.rand(100, 28, 28)
    train_labels = np.random.randint(10, size=(100,))
    model.fit(train_images, train_labels, epochs=1)
    model.save('mnist_model.h5')
    return 'Model trained successfully'

@app.route('/train', methods=['POST'])
def train():
    train_model_async.delay()
    return jsonify({'message': 'Training started'})

@celery.task()
def predict_async(data):
    model = load_model('mnist_model.h5')
    prediction = model.predict(np.array([data]))[0]
    predicted_class = np.argmax(prediction)
    return predicted_class

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    file = request.files['image'].read()
    image = Image.open(io.BytesIO(file)).convert('L')
    image = np.resize(image, (28, 28)) / 255.0
    image = np.array(image, dtype=np.float32)
    task = predict_async.delay(image.tolist())
    return jsonify({'task_id': task.id}), 202


# Define a Resource-type class object to define functions for the RESTful API
class ImageAPI(Resource):

    # GET function, which defines what is sent to the user-side from the server
    @marshal_with(image_definition)
    def get(self, image_id):
        return get_image(image_id)

    # POST function to store image classification data
    @marshal_with(image_definition)
    def post(self, image_id):
        try:
            args = parser.parse_args()

            new_image = ImageClassification(filename=args['filename'], classification=args['classification'])
            with app.app_context():
                db.session.add(new_image)
                db.session.commit()

            process_inference.delay(args['filename'])

            return {'id': new_image.id, 'filename': new_image.filename, 'classification': new_image.classification}
        except Exception as e:
            logging.error(f"Error posting image: {e}")
            print(e)
            return e

    def delete(self, image_id):
        try:
            with app.app_context():
                image = ImageClassification.query.filter_by(id=image_id).first()
                if image:
                    db.session.delete(image)
                    db.session.commit()
                else:
                    return {'error': 'No such image found'}, 404
        except Exception as e:
            logging.error(f"Error deleting image: {e}")
            return e

api.add_resource(ImageAPI, '/image/<int:image_id>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
