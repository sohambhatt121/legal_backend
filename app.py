from flask import Flask, jsonify
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv
import os
import json

from src.routes import initialize_routes

app = Flask(__name__)
api = Api(app)
load_dotenv()

# Swagger configuration
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

# Routes initialization
initialize_routes(api)

# Run Application
if __name__ == '__main__':
    if os.getenv("ENV") == "dev":
        app.run(debug=True)
    else:
        app.run()







