import unittest
from flask_testing import TestCase
from app import create_app
import requests, json, base64
from requests.auth import HTTPBasicAuth

class TestLogin(TestCase):
    TESTING = True

    def create_app(self):
        app = create_app()
        return app

    def runTest(self):  
        url = 'http://localhost:5000/login'
        valid_credentials = base64.b64encode(b'testuser:testpassword').decode('utf-8')
        response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
        self.assertEqual(response.status_code, 200)

    def runTestLoginWithoutAuth(self):
        url = 'http://localhost:5000/login'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 201)

class TestImage(TestCase):

    def create_app(self):
        app = create_app()
        return app
                  
    def setUp(self):  
        url = 'http://localhost:5000/login'
        valid_credentials = base64.b64encode(b'testuser:testpassword').decode('utf-8')
        response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
        response_dict = json.loads(response.data)
        self.token = response_dict['token']
        return self.token

    def runTest(self):
        thumb_url = 'http://localhost:5000/thumbnail?token='+ self.token +'&url=https://homepages.cae.wisc.edu/~ece533/images/airplane.png'
        response1 = requests.get(thumb_url)
        self.assertEqual(response1.status_code, 200)

# class TestPatch(TestCase):
                  
#     def runTest(self):  
#         url = 'http://localhost:5000/login'
#         response = requests.get(url, auth=HTTPBasicAuth('user', 'pass'))
#         if response.ok:
#            token = json.loads(response.text)['token']
#            patch_url = 'http://localhost:5000/patch?token='+ token
#            data = {
#                "json":{
#                "baz": "qux",
#                  "foo": "bar"
#                  },
# 	         "patch":[
#                    { "op": "replace", "path": "/baz", "value": "boo" },
#                    { "op": "add", "path": "/hello", "value": ["world"] },
#                    { "op": "remove", "path": "/foo" }
#                    ]
#                    }
#            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
#            response = requests.patch(patch_url, data=json.dumps(data), headers=headers)
#            str = {
#              "baz": "boo", 
#              "hello": [
#              "world"
#              ]
#              }
#            self.assertEqual(json.loads(response.text), str)
#            self.assertEqual(response.status_code, 200)
        
suite = unittest.TestSuite()

if __name__ == '__main__':
    unittest.main()

