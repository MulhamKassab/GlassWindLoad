from flask import Flask
from flask_cors import CORS

# Import Blueprints
from routes.calculate import calculate_bp
from routes.download import download_bp

def create_app():
    app = Flask(__name__)
    CORS(app)  # Allow cross-origin requests for local React dev

    # Register Blueprints
    app.register_blueprint(calculate_bp, url_prefix='/api')
    app.register_blueprint(download_bp, url_prefix='/api')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
