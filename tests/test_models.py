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
        call = VideoCall(
            user_id=1,
            duration=30,
            resolution='720p',
            connection_speed=100,
            device_specs={'cpu': 'Intel', 'ram': '8GB'}
        )
        db.session.add(call)
        db.session.commit()

        self.assertEqual(VideoCall.query.count(), 1)

if __name__ == '__main__':
    unittest.main()
