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
        # Add assertions for response content if applicable
        # Example: self.assertIn('expected_key', response.json)

    def test_add_call(self):
        response = self.client.post('/add_call', json={
            'user_id': 1,
            'duration': 30,
            'resolution': '720p',
            'connection_speed': 100,
            'device_specs': {'cpu': 'Intel', 'ram': '8GB'}
        })
        self.assertEqual(response.status_code, 201)

        # Check if the VideoCall was added to the database
        self.assertEqual(VideoCall.query.count(), 1)

        # Retrieve the added VideoCall
        added_call = VideoCall.query.first()

        # Verify the fields
        self.assertEqual(added_call.user_id, 1)
        self.assertEqual(added_call.duration, 30)
        self.assertEqual(added_call.resolution, '720p')
        self.assertEqual(added_call.connection_speed, 100)
        self.assertEqual(added_call.device_specs, {'cpu': 'Intel', 'ram': '8GB'})

    def test_add_call_invalid_data(self):
        response = self.client.post('/add_call', json={
            'user_id': 'invalid',  # Invalid user_id
            'duration': 'invalid',  # Invalid duration
            'resolution': 'unknown',  # Invalid resolution
            'connection_speed': 'invalid',  # Invalid connection_speed
            'device_specs': 'invalid'  # Invalid device_specs
        })
        self.assertEqual(response.status_code, 400)
        # Add assertions for the response error message if applicable
        # Example: self.assertIn('error_message', response.json)

if __name__ == '__main__':
    unittest.main()
