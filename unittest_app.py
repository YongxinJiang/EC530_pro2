import unittest
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

    def test_train_route(self):
        response = self.app.post('/train')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Training started', response.data)

    def test_predict_route(self):
        # Assuming image file is provided in the request
        response = self.app.post('/predict', data={'image': (b'test_image.jpg', b'data')})
        self.assertEqual(response.status_code, 202)
        self.assertIn(b'task_id', response.data)

if __name__ == '__main__':
    unittest.main()
