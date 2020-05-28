from flaskr import create_app, settings
from flask import request, jsonify
from flask_bcrypt import Bcrypt
from flaskr.models import User
from flask_jsonschema_validator import JSONSchemaValidator

app = create_app()
becrypt = Bcrypt(app)

if __name__ == '__main__':
    app.run(
        host=settings.BIND_HOST,
        port=settings.BIND_PORT,
        debug=settings.DEBUG,
    )
