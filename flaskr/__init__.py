from flask import Flask, jsonify
from flask_graphql import GraphQLView
from .schemas import schema
from flask_jsonschema_validator.jsonschemavalidator import JSONSchemaValidator
from flask_graphql_auth import GraphQLAuth
import jsonschema
from flask_cors import CORS

def create_app(test_config=None):
    app = Flask(__name__)
    app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
        'graphql', schema=schema, graphiql=True
    ))

    GraphQLAuth(app)
    CORS(app)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 60
    app.config['JWT_SECRET_KEY'] = 'aVerySecretJwtSigningKey'

    JSONSchemaValidator(app=app,root="schemas")

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({'message': 'The requested URL was not found on the server.'}), 404

    return app