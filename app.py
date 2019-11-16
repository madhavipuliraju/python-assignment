from flask import Flask, request, make_response, jsonify
import jwt

app = Flask(__name__)

app.config['SECRET_KEY'] = "this is the secret key"
		

@app.route('/unprotected')
def unprotected():
	return 'unprotected'

@app.route('/login')
def login():
	auth = request.authorization
	if authorization:
		token = jwt.encode({'user':auth.username},'secret', algorithm='HS256')
		return jsonify({'token':token})

	return make_response("Un Authorized", 401, {'WWW-Authenticate':'Basic-realm="Login required!"'})


if __name__ == '__main__':
	app.run(debug=True)