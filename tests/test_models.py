import unittest
from app import create_app, db
from app.models import VideoCall

class ModelsTestCase(unittest.TestCase):
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

    def test_video_call_model(self):
        # Create a VideoCall instance
        call = VideoCall(
            user_id=1,
            duration=30,
            resolution='720p',
            connection_speed=100,
            device_specs={'cpu': 'Intel', 'ram': '8GB'}
        )
        db.session.add(call)
        db.session.commit()

        # Check that the VideoCall was added to the database
        self.assertEqual(VideoCall.query.count(), 1)

        # Retrieve the VideoCall from the database
        retrieved_call = VideoCall.query.first()
        
        # Check that the fields are correctly set
        self.assertEqual(retrieved_call.user_id, 1)
        self.assertEqual(retrieved_call.duration, 30)
        self.assertEqual(retrieved_call.resolution, '720p')
        self.assertEqual(retrieved_call.connection_speed, 100)
        self.assertEqual(retrieved_call.device_specs, {'cpu': 'Intel', 'ram': '8GB'})

if __name__ == '__main__':
    unittest.main()
