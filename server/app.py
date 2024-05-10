from flask import Flask, make_response, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Organization , User, Donation, Story
# from flask_bcrypt import Bcrypt

app = Flask(__name__)
CORS(app)


app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mazingira.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)
# bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return '<h1>Welcome To Mazingira</h1>'

# Admin Endpoints

class AdminOrganizations(Resource):
    def get(self):
        try:
            orgs = []
            for organization in Organization.query.all():
                orgs.append({
                    'id': organization.id,
                    'name': organization.name,
                    'email': organization.email,
                    'image_url': organization.image_url,
                    'approval_status': organization.approval_status,
                    'description': organization.description,
                })
            if orgs:
                return make_response(jsonify({'message': 'success', 'data': orgs}), 200)
            else:
                return make_response(jsonify({'message': 'No Organizations Found'}), 404)
        except Exception as e:
            return make_response(jsonify({'message': 'An error occurred', 'error': str(e)}), 500)
        
class AdminOrganizationByID(Resource):

    # View One Organization as the Admin
    def get(self, id):
        organization = Organization.query.filter(Organization.id == id).first()
        if organization is None:
            return make_response(jsonify({'message': 'The requested Organization does not exist'}), 404)
        else:
            return make_response(jsonify({
                'id': organization.id,
                'name': organization.name,
                'email': organization.email,
                'image_url': organization.image_url,
                'approval_status': organization.approval_status,
                'description': organization.description,
            }), 200)
        
    def patch(self, id):
        # Approve/Update an existing Organization

        organization = Organization.query.filter(Organization.id == id).first()
        if not organization:
            return {'message': 'Organization not found'}, 404

        for attr in request.json:
            setattr(organization, attr, request.json[attr])

        db.session.commit()
        return {'message': 'Organization Updated Successfully', 'organization': {
            'id': organization.id,
            'name': organization.name,
            'email': organization.email,
            'image_url': organization.image_url,
            'approval_status': organization.approval_status,
            'description': organization.description,
        }}, 200
    
    def delete(self, id):
        organization = Organization.query.filter_by(id=id).first()
        if organization:
            db.session.delete(organization)
            db.session.commit()
            return {'message': 'Organization deleted successfully'}, 200
        else:
            return {'message': 'Organization not found'}, 404

# Donor Endpoints

class DonorOrganizations(Resource):

    def get(self):
        try:
            orgs = []
            for organization in Organization.query.filter_by(approval_status = True).all():
                orgs.append({
                    'id': organization.id,
                    'name': organization.name,
                    'email': organization.email,
                    'image_url': organization.image_url,
                    'approval_status': organization.approval_status,
                    'description': organization.description,
                })
            if orgs:
                return make_response(jsonify({'message': 'success', 'data': orgs}), 200)
            else:
                return make_response(jsonify({'message': 'No Organizations Found'}), 404)
        except Exception as e:
            return make_response(jsonify({'message': 'An error occurred', 'error': str(e)}), 500)
        
class DonorOrganizationByID(Resource):

    def get(self, id):
        organization = Organization.query.filter(Organization.id == id, Organization.approval_status == True).first()
        if organization is None:
            return make_response(jsonify({'message': 'The requested Organization does not exist'}), 404)
        else:
            return make_response(jsonify({
                'id': organization.id,
                'name': organization.name,
                'email': organization.email,
                'image_url': organization.image_url,
                'approval_status': organization.approval_status,
                'description': organization.description,
            }), 200)
        

class Donate(Resource):

    def post(self):
        
        donation = Donation(
            amount=request.json['amount'],
            anonymous=request.json['anonymous'],
            donor_id = request.json['donor_id'],
            organization_id = request.json['organization_id'])
        db.session.add(donation)
        db.session.commit()
        return make_response(jsonify({
            'id': donation.id,
            'amount': donation.amount,
            'anonymous': donation.anonymous,
            'donor_id': donation.donor_id,
            'organization_id': donation.organization_id
        }), 200)


# Organizations Endpoints

class OrganizationDashboard(Resource):
    
    def get(self):
        pass



# EndPoints
api.add_resource(AdminOrganizations, '/admin', endpoint='admin_organizations')
api.add_resource(AdminOrganizationByID, '/admin/<int:id>', endpoint='admin_organizations_by_id')
api.add_resource(OrganizationDashboard, '/organization', endpoint='organization_dashboard')
api.add_resource(DonorOrganizations, '/donor/organization', endpoint='donor_organizations')
api.add_resource(DonorOrganizationByID, '/donor/organization/<int:id>', endpoint='donor_organization_by_id')
api.add_resource(Donate, '/donate', endpoint='donate')

if __name__ == '__main__':
    app.run(port=5555, debug=True)