import unittest
import json
from app import app, db, ImageClassification

class TestApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_image(self):
        img = ImageClassification(filename="test_image.jpg", classification="cat")
        db.session.add(img)
        db.session.commit()

        response = self.app.get('/image/1')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['filename'], "test_image.jpg")
        self.assertEqual(data['classification'], "cat")

    def test_post_image(self):
        response = self.app.post('/image/1', json={"filename": "new_image.jpg", "classification": "dog"})
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['filename'], "new_image.jpg")
        self.assertEqual(data['classification'], "dog")

        img = ImageClassification.query.filter_by(filename="new_image.jpg").first()
        self.assertIsNotNone(img)

    def test_delete_image(self):
        img = ImageClassification(filename="test_image.jpg", classification="cat")
        db.session.add(img)
        db.session.commit()

        response = self.app.delete('/image/1')

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(ImageClassification.query.filter_by(filename="test_image.jpg").first())

if __name__ == '__main__':
    unittest.main()
