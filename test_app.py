import unittest
import requests, json, base64
from requests.auth import HTTPBasicAuth

class TestLogin(unittest.TestCase):
                  
    def runTest(self):  
        url = 'http://localhost:5000/login'
        response = requests.get(url, auth=HTTPBasicAuth('user', 'pass'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.ok)

    def runTestLoginWithoutAuth(self):
        url = 'http://localhost:5000/login'
        response = requests.get(url)
        self.assertEqual(response.status_code, 401)

class TestImage(unittest.TestCase):
                  
    def runTest(self):  
        url = 'http://localhost:5000/login'
        response = requests.get(url, auth=HTTPBasicAuth('user', 'pass'))
        if response.ok:
           token = json.loads(response.text)['token']
           thumb_url = 'http://localhost:5000/thumnail?token='+ token +'&url=https://homepages.cae.wisc.edu/~ece533/images/airplane.png'
           print (thumb_url)
           response = requests.get(thumb_url)
           self.assertEqual(response.status_code, 200)

class TestPatch(unittest.TestCase):
                  
    def runTest(self):  
        url = 'http://localhost:5000/login'
        response = requests.get(url, auth=HTTPBasicAuth('user', 'pass'))
        if response.ok:
           token = json.loads(response.text)['token']
           patch_url = 'http://localhost:5000/patch?token='+ token
           data = {
               "json":{
               "baz": "qux",
                 "foo": "bar"
                 },
	         "patch":[
                   { "op": "replace", "path": "/baz", "value": "boo" },
                   { "op": "add", "path": "/hello", "value": ["world"] },
                   { "op": "remove", "path": "/foo" }
                   ]
                   }
           headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
           response = requests.patch(patch_url, data=json.dumps(data), headers=headers)
           str = {
             "baz": "boo", 
             "hello": [
             "world"
             ]
             }
           self.assertEqual(json.loads(response.text), str)
           self.assertEqual(response.status_code, 200)
        
suite = unittest.TestSuite()

if __name__ == '__main__':
    unittest.main()

