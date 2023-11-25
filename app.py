from flask import Flask, jsonify
from database.db import db
from flask_restful import Api
from src.routes import initialize_routes
from flask_swagger_ui import get_swaggerui_blueprint
import json

app = Flask(__name__)
api = Api(app)

SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Legal Software APIs"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
@app.route('/swagger.json')
def swagger():
    with open('swagger.json', 'r') as f:
        return jsonify(json.load(f))

initialize_routes(api)

app.run(debug=True)







