import unittest
from app import create_app, db
from app.models import VideoCall

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_data(self):
        response = self.client.get('/data')
        self.assertEqual(response.status_code, 200)

    def test_add_call(self):
        response = self.client.post('/add_call', json={
            'user_id': 1,
            'duration': 30,
            'resolution': '720p',
            'connection_speed': 100,
            'device_specs': {'cpu': 'Intel', 'ram': '8GB'}
        })
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()
