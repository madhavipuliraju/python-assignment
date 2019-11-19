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
        #credentials = base64.b64encode(bytes('username'+':'+'password','ascii')).decode('ascii')
        valid_credentials = base64.b64encode(b'testuser:testpassword').decode('utf-8')
        #self.client.defaults['HTTP_AUTHORIZATION'] = 'Basic ' + credentials
        #headers = {'HTTP_AUTHORIZATION':'Basic' + base64.b64encode(bytes('username'+':'+'password','ascii')).decode('ascii')}
        response = self.client.get(url, headers={'Authorization': 'Basic ' + valid_credentials})
        #response = requests.get(url, auth=HTTPBasicAuth('user', 'pass'))
        self.assertEqual(response.status_code, 200)


    def runTestLoginWithoutAuth(self):
        url = 'http://localhost:5000/login'
        response = requests.get(url)
        self.assertEqual(response.status_code, 401)

# class TestImage(TestCase):
                  
#     def runTest(self):  
#         url = 'http://localhost:5000/login'
#         response = requests.get(url, auth=HTTPBasicAuth('user', 'pass'))
#         if response.ok:
#            token = json.loads(response.text)['token']
#            thumb_url = 'http://localhost:5000/thumnail?token='+ token +'&url=https://homepages.cae.wisc.edu/~ece533/images/airplane.png'
#            print (thumb_url)
#            response = requests.get(thumb_url)
#            self.assertEqual(response.status_code, 200)

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
        
# suite = unittest.TestSuite()

if __name__ == '__main__':
    unittest.main()

