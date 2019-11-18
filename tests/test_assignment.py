import unittest
import requests, json

class TestLogin(unittest.TestCase):
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

class TestPatch(unittest.TestCase):
    def runTest(self):  
    	base_url = 'http://localhost:5000/login'
    	response1 = requests.get(base_url, auth=('testuser','password'))
    	if response1.ok:
    		data = json.loads(response1.text)
    		token = data['token']
    		url = "http://localhost:5000/patch?token=" + token
    		input_data = {"json":{"baz": "qux","foo": "bar"}, "patch":[
 									{ "op": "replace", "path": "/baz", "value": "boo" },
  									{ "op": "add", "path": "/hello", "value": ["world"] },
  									{ "op": "remove", "path": "/foo" }
								]
						}
    		response2 = requests.patch(url, input_data, headers = {'X-HTTP-Method-Override':'PATCH'})
    		print response2.text
        	self.assertTrue(response2.ok)

	def runTestLoginWithoutAuth(self):  
		url = 'http://localhost:5000/login'
    	response = requests.get(url)
    	self.assertEqual(response.status_code, 401)



suite = unittest.TestSuite()

if __name__ == '__main__':
    unittest.main()
