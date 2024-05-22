from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mazingira.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Roles: 'donor', 'organization', 'administrator'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Organization(db.Model):
    __tablename__ = 'organizations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    image_url = db.Column(db.String(255))
    learn_more = db.Column(db.String(255))

class Donation(db.Model):
    __tablename__ = 'donations'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    donor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    anonymous = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False)

class Beneficiary(db.Model):
    __tablename__ = 'beneficiaries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

class Story(db.Model):
    __tablename__ = 'stories'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

# User Registration
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not email or not password or not role:
        return jsonify({'message': 'Missing required fields'}), 400

    # Check if the email already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 409

    # Create a new user
    new_user = User(email=email, role=role)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


# User Login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Missing email or password'}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid email or password'}), 401

    # Generate JWT token
    token = jwt.encode({'user_id': user.id, 'role': user.role, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'])

    print("Generated token:", token)  # Add this line for debugging

    return jsonify({'token': token}), 200


# Authentication Middleware
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

# Get Organizations
@app.route('/api/organizations', methods=['GET'])
def get_organizations():
    organizations = Organization.query.all()
    result = [{'id': org.id, 'name': org.name, 'image_url': org.image_url, 'learn_more': org.learn_more} for org in organizations]
    return jsonify(result)

# Donate
@app.route('/api/donate', methods=['POST'])
@token_required
def donate(current_user):
    data = request.get_json()
    organization_id = data.get('organization_id')
    amount = data.get('amount')
    is_anonymous = data.get('is_anonymous', False)

    if not organization_id or not amount:
        return jsonify({'message': 'Missing required fields'}), 400

    # Check if organization exists
    organization = Organization.query.get(organization_id)
    if not organization:
        return jsonify({'message': 'Organization not found'}), 404

    # Create new donation
    new_donation = Donation(amount=amount, donor_id=current_user.id, organization_id=organization_id, anonymous=is_anonymous)
    db.session.add(new_donation)
    db.session.commit()

    return jsonify({'message': 'Donation successful'}), 201

# if __name__ == '__main__':
#     db.create_all()
#     app.run(debug=True)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)



