from flaskr import create_app, settings
from flask import request, jsonify
from flask_bcrypt import Bcrypt
from flaskr.models import User
from flask_jsonschema_validator import JSONSchemaValidator

app = create_app()
becrypt = Bcrypt(app)

@app.route('/register', methods=['POST'])
@app.validate('users', 'register')
def register():
   data = request.get_json()
   if User(username=data['username']).fetch() is not None:
      return jsonify({"message": "User already exists"}),400
   pwhash = becrypt.generate_password_hash(data['password'])
   User(username=data['username'], passwordHash=pwhash).save()
   return jsonify({"message": "Successfully created new user"}),200
   

@app.route('/login', methods=['POST'])
@app.validate('users','register')
def login():
   data = request.get_json()
   user = User(username=data['username']).fetch()
   if user is None:
      return jsonify({"message": "User not found"}),404
   
   if not (becrypt.check_password_hash(user.passwordHash, data['password'])):
      return jsonify({"message": "Wrong password"}),401

   return "login endpoint."

if __name__ == '__main__':
    app.run(
        host=settings.BIND_HOST,
        port=settings.BIND_PORT,
        debug=settings.DEBUG,
    )