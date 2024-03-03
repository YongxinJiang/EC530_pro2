import os
import logging
from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

log_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.log')
logging.basicConfig(filename=log_file, level=logging.INFO)

api = Api(app)

database_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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

class ImageAPI(Resource):

    @marshal_with(image_definition)
    def get(self, image_id):
        return get_image(image_id)

    @marshal_with(image_definition)
    def post(self, image_id):
        try:
            args = parser.parse_args()

            new_image = ImageClassification(filename=args['filename'], classification=args['classification'])
            with app.app_context():
                db.session.add(new_image)
                db.session.commit()

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



