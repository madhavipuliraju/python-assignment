from app import *
import unittest
import requests, json

class TestLogin(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
    def runTest(self):  
        url = 'http://localhost:5000/login'
        response = requests.get(url, auth=('testuser','password'))
        data = json.loads(response.text)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)

    def runTestLoginWithoutAuth(self):
        url = 'http://localhost:5000/login'
        response = requests.get(url)
        self.assertEqual(response.status_code, 401)


suite = unittest.TestSuite()

if __name__ == '__main__':
    unittest.main()

