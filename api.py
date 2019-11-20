from flask import Flask, request, make_response, jsonify, abort
from flask import send_file, Blueprint, current_app
import jwt
import datetime
from functools import wraps
import json, requests, jsonpatch
import glob
from PIL import Image
from io import BytesIO

api = Blueprint('APIs', __name__)

#file_handler = logging.FileHandler('current_app.log')
#current_app.logger.addHandler(file_handler)
#current_app.logger.setLevel(logging.INFO)
#current_app.logger.setLevel(logging.ERROR)

def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = request.args.get('token')
		current_app.logger.info('token is %s' %token)
		if not token:
			current_app.logger.error('Token is missing' )
			return jsonify({'message': 'Token is missing'}), 403
		try:
			data = jwt.decode(token, current_app.config['SECRET_KEY'])
			current_app.logger.info('Data after decode: %s' % json.dumps(data))
		except:
			current_app.logger.error('Invalid Token')
			return jsonify({'message': 'Invalid Token'}), 403
		return f(*args, **kwargs)
	return decorated

@api.route('/patch', methods=['PATCH'])
@token_required
def patch():
    json_object = request.json['json']
    if not json_object:
        current_app.logger.error('JSON object is missing in the payload')
        return jsonify({'message': 'Key Error: json key is missing'}), 500

    patch = request.json['patch']
    if not patch:
        current_app.logger.error('JSON patch object is missing in the payload' )
        return jsonify({'message': 'Key Error: patch key is missing'}), 403

    res = jsonpatch.apply_patch(json_object, patch)
    return res

@api.route('/thumbnail')
@token_required
def thumbnail():
    url= request.args.get('url')
    current_app.logger.info('Image url is %s' %url)
    if not url:
    	current_app.logger.error('Image URL is missing')
    	return jsonify({'message': 'Image URL is missing'}), 403
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    current_app.logger.info('image opened')
    im = img.convert('RGB')
    current_app.logger.info('image converted to RGB')# convert to thumbnail image
    im.thumbnail((50, 50), Image.ANTIALIAS)
    current_app.logger.info('image size converted to 50*50')
    im.save('thumbnail', "JPEG")
    return send_file("thumbnail", mimetype='image/jpeg')
	

@api.route('/login')
def login():
	auth = request.authorization
	if auth and auth.username and auth.password:
		current_app.logger.info('authentication sucessful')
		token = jwt.encode({'user':auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, current_app.secret_key)
		return jsonify({'token':token})


	current_app.logger.error('Unauthorized. Please enter Username and Password to login')
	return make_response('Un Authorized', 401, {'WWW-Authenticate':'Basic-realm="Login required!"'})

@api.route('/')
def deployment():
    return jsonify({"message": "Deployment sucessful"})
