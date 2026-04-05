import unittest
from app import app

class FlaskAppTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.app.post('/login', data=dict(
            username="admin",
            password="1234"
        ), follow_redirects=True)
        self.assertIn(b'Dashboard', response.data)

if __name__ == "__main__":
    unittest.main()