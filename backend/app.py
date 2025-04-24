from flask import Flask
from flask_cors import CORS

# Import Blueprints
from routes import all_blueprints


def create_app():
    app = Flask(__name__)
    CORS(app)  # Allow cross-origin requests for local React dev

    for bp in all_blueprints:
        app.register_blueprint(bp, url_prefix='/api')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
