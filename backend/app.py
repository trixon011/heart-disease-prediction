from flask import Flask, request, jsonify
from flask_cors import CORS
from model import predict
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)

# 🔧 Set this to your actual frontend URL
FRONTEND_ORIGIN = 'https://heart-disease-prediction-2-1a8c.onrender.com'

# ✅ CORS: Allow only the frontend origin + support credentials & preflight
CORS(app, resources={r"/api/*": {"origins": FRONTEND_ORIGIN}}, supports_credentials=True)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# 📦 User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

# 🔧 Create DB tables
with app.app_context():
    db.create_all()

# 🧾 Signup route
@app.route('/api/signup', methods=['POST', 'OPTIONS'])
def signup():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'Preflight passed'}), 200

    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if not all([name, email, password]):
            return jsonify({'error': 'Name, email and password are required.'}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'User already exists.'}), 400

        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(name=name, email=email, password_hash=pw_hash)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User created successfully.'}), 200

    except Exception as e:
        print("Signup error:", e)
        return jsonify({'error': 'Internal server error'}), 500

# 🔐 Login route
@app.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'Preflight passed'}), 200

    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        print("Login attempt:", email)

        if not all([email, password]):
            return jsonify({'error': 'Email and password are required.'}), 400

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            return jsonify({'message': 'Login successful.'}), 200

        return jsonify({'error': 'Invalid email or password.'}), 401

    except Exception as e:
        print("Login error:", e)
        return jsonify({'error': 'Internal server error'}), 500

# 🧠 Prediction route
@app.route('/api/predict', methods=['POST', 'OPTIONS'])
def predict_route():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'Preflight passed'}), 200

    try:
        data = request.get_json()
        print("Received JSON:", data)

        if not data or "input" not in data:
            return jsonify({'error': "Missing 'input' in JSON"}), 400

        input_data = data["input"]

        if not isinstance(input_data, list) or len(input_data) != 13:
            return jsonify({'error': "Input must be a list of 13 numbers"}), 400

        result = predict(input_data)

        print("Prediction result:", result)

        return jsonify(result)

    except Exception as e:
        print("Prediction error:", e)
        return jsonify({'error': str(e)}), 500

# 🚀 Run app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
