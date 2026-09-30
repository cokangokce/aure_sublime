from flask import Flask
from flask_cors import CORS
from database import init_db
from routes import api_bp

app = Flask(__name__)
CORS(app)

init_db()

app.register_blueprint(api_bp)

if __name__ == '__main__':
    print("Aurae Sublime Backend Calisiyor...")
    app.run(host='0.0.0.0', port=5000, debug=True)