from flask import Flask, request, make_response, jsonify
import jwt
import datetime
from functools import wraps
import logging
import json

app = Flask(__name__)

file_handler = logging.FileHandler('app.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
#app.logger.setLevel(logging.ERROR)

app.config['SECRET_KEY'] = "this is the secret key"
		
def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = request.args.get('token')
		app.logger.info('token is %s' %token)
		if not token:
			app.logger.error('Token is missing' )
			return jsonify({'message': 'Token is missing'}), 403
		try:
			data = jwt.decode(token, app.config['SECRET_KEY'])
			app.logger.info('Data after decode: %s' % json.dumps(data))
		except:
			app.logger.error('Invalid Token')
			return jsonify({'message': 'Invalid Token'}), 403
		return f(*args, **kwargs)
	return decorated

@app.route('/protected')
@token_required
def protected():
	return 'protected'

@app.route('/login')
def login():
	auth = request.authorization
	if auth and auth.username and auth.password:
		app.logger.info('authentication sucessful')
		token = jwt.encode({'user':auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
		return jsonify({'token':token})


	app.logger.error('Unauthorized. Please enter Username and Password to login')
	return make_response('Un Authorized', 401, {'WWW-Authenticate':'Basic-realm="Login required!"'})


if __name__ == '__main__':
	app.run(debug=True)