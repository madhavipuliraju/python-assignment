from flask import Flask, request, make_response, jsonify
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = "this is the secret key"
		
def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = request.args.get('token')
		print token
		if not token:
			return jsonify({'message': 'Token is missing'}), 403
		try:
			data = jwt.decode(token, app.config['SECRET_KEY'])
		except:
			return jsonify({'message': 'Token is invalid'}), 403
		return f(*args, **kwargs)
	return decorated

@app.route('/protected')
@token_required
def protected():
	return 'protected'

@app.route('/login')
def login():
	auth = request.authorization
	if auth:
		token = jwt.encode({'user':auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
		return jsonify({'token':token})

	return make_response("Un Authorized", 401, {'WWW-Authenticate':'Basic-realm="Login required!"'})


if __name__ == '__main__':
	app.run(debug=True)