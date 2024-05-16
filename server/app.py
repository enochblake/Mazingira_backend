import os

from flask import Flask, make_response, jsonify, request, session, redirect
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Organization , User, Donation, Story, Beneficiary

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mazingira.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.json.compact = False

app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

# @app.before_request
# def check_if_logged_in():
#     allowed_admin_endpoints = ['logout','admin_organizations', 'admin_organizations_by_id', 'checksession' ]
#     allowed_donor_endpoints = ['logout','donor_organizations', 'donor_organization_by_id', 'donate', 'beneficiaries_stories', 'checksession']
#     allowed_organization_endpoints = ['logout','organization_dashboard', 'set_up_organization_details', 'non_anonymous_donations', 'create_post', 'create_beneficiary', 'checksession']

#     if session.get('user_id'):
#         if session.get('user_role') == 'donor':
#             if request.endpoint not in allowed_donor_endpoints:
#                 return {'error': 'Unauthorized To Access This Resource'}, 401
#         elif session.get('user_role') == 'admin':
#             if request.endpoint not in allowed_admin_endpoints:
#                 return {'error': 'Unauthorized To Access This Resource'}, 401
#         # elif session.get('user_role') == 'org':
#         else:
#             if request.endpoint not in allowed_organization_endpoints:
#                 return {'error': 'Unauthorized To Access This Resource'}, 401
#     else:
#         if request.endpoint not in ['checksession','organization_login', 'login', 'home', 'register_user', 'register_organization']:
#             return {'error': 'Unauthorized Log In First'}, 401

@app.route('/')
def index():
    return '<h1>Welcome To Mazingira</h1>'

# AUTHENTICATION

class UserLogin(Resource):

    def post(self):
        data = request.get_json()
        if data:
            email = request.get_json()['email']
            user = User.query.filter(User.email == email).first()
            password = request.get_json()['password']
            
            if user and user.authenticate(password) == True:
                # print(user.authenticate(password))
                session['user_id'] = user.id
                session['user_role'] = user.role
                # user_dict = {
                # 'id': user.id,
                # 'first_name': user.first_name,
                # 'last_name': user.last_name,
                # 'email': user.email,
                # 'role': user.role,
                # }
                # return make_response(user_dict, 200)
                if user.role == 'donor':
                    return redirect('donor/organization')
                else:
                    return redirect('/admin')
            else:
                return make_response({'error': 'Invalid username or password'}, 401)

class RegisterUser(Resource):

    def post(self):

        data = request.get_json()
        if data:
            first_name = request.get_json()['first_name']
            last_name = request.get_json()['last_name']
            email = request.get_json()['email']
            password = request.get_json()['password']

            new_user = User(first_name=first_name, last_name=last_name, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()

            user = User.query.filter(User.email == email).first()
            if user and user.authenticate(password) == True:
                session['user_id'] = user.id
                session['user_role'] = user.role

                user_dict = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'role': user.role,
                }
                return make_response(user_dict, 200)
            
            resp = {'message': f'Congratulations {first_name} {last_name}! Successfully Registered'}
            return make_response(resp, 201)
            # return redirect('/login')
        else:
            return make_response({'message': 'All fields have to be filled'}, 401)


class RegisterOrganization(Resource):

    def post(self):

        data = request.get_json()
        if data:
            name = request.get_json()['name']
            email = request.get_json()['email']
            password = request.get_json()['password']

            new_org = Organization(name=name, email=email)
            new_org.set_password(password)
            db.session.add(new_org)
            db.session.commit()

            org = Organization.query.filter(Organization.email == email).first()

            if org and org.authenticate(password) == True:
                session['user_id'] = org.id
                session['user_role'] = org.role
                org_dict = {
                'id': org.id,
                'name': org.name,
                'email': org.email
                }
                return make_response(org_dict, 200)
                # return redirect('/organization')
            else:
                return make_response({'error': 'Invalid username or password'}, 401)
        else:
            return make_response({'message': 'All fields have to be filled'}, 401)

class OrganizationLogin(Resource):

    def post(self):
        data = request.get_json()
        if data:
            email = request.get_json()['email']
            org = Organization.query.filter(Organization.email == email).first()
            password = request.get_json()['password']
            
            if org and org.authenticate(password) == True:
                # print(user.authenticate(password))
                session['user_id'] = org.id
                session['user_role'] = org.role
                return redirect('/organization')
            else:
                return make_response({'error': 'Invalid username or password'}, 401)
class CheckSession(Resource):

    def get(self):
        if session.get('user_id') and session['user_role'] != 'org':
            user = User.query.filter(User.id == session.get('user_id')).first()
            user_dict = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'role': user.role,
                }
            return make_response(user_dict, 200)
        elif session.get('user_id') and session['user_role'] == 'org':
            org = Organization.query.filter(Organization.id == session.get('user_id')).first()
            org_dict = {
                'id': org.id,
                'name': org.name,
                'approval_status': org.approval_status,
                'email': org.email,
                'description': org.description,
                'category': org.category,
                'history': org.history,
                'image_url': org.image_url,
                'registered_on': org.created_at,
                'application_reviewed_on': org.updated_at
                }
            return make_response(org_dict, 200)
        else:
            return {'message': 'Log In To Access Resource or Contact Mazingira'}, 401
class Logout(Resource):

    def delete(self):
        session['user_id'] = None
        session['user_role'] = None
        return {'message': '204: No Content'}, 204

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
                    'history': organization.history,
                    'category': organization.category,
                    'updated_at': organization.updated_at
                })
            if orgs:
                return make_response(jsonify(orgs), 200)
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
                'category': organization.category,
                'history': organization.history,
                'updated_at': organization.updated_at
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
            'history': organization.history,
            'category': organization.category
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
                    'logo': organization.image_url,
                    'approval_status': organization.approval_status,
                    'description': organization.description,
                    'history': organization.history,
                    'category': organization.category
                })
            if orgs:
                return make_response(jsonify(orgs), 200)
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
                'logo': organization.image_url,
                'approval_status': organization.approval_status,
                'description': organization.description,
                'history': organization.history,
                'category': organization.category,
            }), 200)
        

class Donate(Resource):

    def post(self):
        
        donation = Donation(
            amount=request.json['amount'],
            anonymous=request.json['anonymous'],
            donor_id = session['user_id'],                  
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
    
class BeneficiariesStories(Resource):

    def get(self):
        try:
            user = User.query.filter(User.id == session['user_id']).first()
            stories = []
            for story in user.donated_stories():
                stories.append({
                    'id': story.id,
                    'title': story.title,
                    'content': story.content,
                    'image_url': story.image_url,
                    'time_to_read': story.time_to_read,
                    'created_at': story.created_at,
                    'organization_id': story.organization_id,
                })
            if stories:
                return make_response(jsonify(stories), 200)
            else:
                return make_response(jsonify({'message': 'No Stories Found. Make A Donation First'}), 404)
        except Exception as e:
            return make_response(jsonify({'message': 'An error occurred', 'error': str(e)}), 500)


# Organizations Endpoints

class OrganizationDashboard(Resource):
    
    # View Organization Details

    def get(self):
        org = Organization.query.filter(Organization.id == session.get('user_id')).first()
        org_dict = {
            'id': org.id,
            'name': org.name,
            'approval_status': org.approval_status,
            'email': org.email,
            'description': org.description,
            'image_url': org.image_url,
            'registered_on': org.created_at,
            'category': org.category,
            'history': org.history,
            'application_reviewed_on': org.updated_at
            }
        return make_response(org_dict, 200)

    # Set Up Organization Details
class SetUpOrganizationDetails(Resource):

    def patch(self):
        # Edit/Setup an approved Organization
        organization = Organization.query.filter(Organization.id == session['user_id']).first()
        if not organization:
            return {'message': 'Organization not approved or found. Contact Admin'}, 404
        
        for attr in request.json:
            setattr(organization, attr, request.json[attr])

        db.session.commit()
        return {'message': 'Organization Updated Successfully', 'organization': {
            'id': organization.id,
            'name': organization.name,
            'email': organization.email,
            'image_url': organization.image_url,
            'approval_status': organization.approval_status,
            'category': organization.category,
            'description': organization.description,
            'history': organization.history
        }}, 200

class OrganizationDonations(Resource):
    
    def get(self):
        try:
            donations = []
            for donation in Donation.query.filter_by(organization_id = session['user_id']):
                user = User.query.get(donation.donor_id)
                donations.append({
                    'id': donation.id,
                    'amount': donation.amount,
                    'donated_on': donation.created_at,
                    'organization_id': donation.organization_id,
                    'anonymous_status': donation.anonymous,
                    'donor_first_name': user.first_name,
                    'donor_last_name': user.last_name
                })
            if donations:
                return make_response(jsonify(donations), 200)
            else:
                return make_response(jsonify({'message': 'No Donations Found'}), 404)
        except Exception as e:
            return make_response(jsonify({'message': 'An error occurred', 'error': str(e)}), 500)
        
class OrganizationCreateStories(Resource):

    def post(self):
        
        story = Story(
            title=request.json['title'],
            content=request.json['content'],
            image_url=request.json['image_url'],
            beneficiary_id=request.json['beneficiary_id'],
            time_to_read=request.json['time_to_read'],
            organization_id=session['user_id']
        )
        db.session.add(story)
        db.session.commit()

        beneficiary = Beneficiary.query.get(story.beneficiary_id)

        return make_response(jsonify({
            'id': story.id,
            'title': story.title,
            'content': story.content,
            'image_url': story.image_url,
            'time_to_read':story.time_to_read,
            'organization_id': story.organization_id,
            'created_at': story.created_at,
            'beneficary_name': beneficiary.name,
            'beneficary_image': beneficiary.image_url,
            'beneficary_amount': beneficiary.recieved_amount
        }), 200)
    
class OrgCreateBeneficiary(Resource):

    def get(self):
        try:
            beneficiaries = []
            for beneficiary in Beneficiary.query.filter_by(organization_id = session['user_id']):
                # user = User.query.get(donation.donor_id)
                beneficiaries.append({
                    'id': beneficiary.id,
                    'name': beneficiary.name,
                    'recieved_amount': beneficiary.recieved_amount,
                    'organization_id': beneficiary.organization_id,
                    'image_url': beneficiary.image_url
                })
            if beneficiaries:
                return make_response(jsonify(beneficiaries), 200)
            else:
                return make_response(jsonify({'message': 'No Organizations Found'}), 404)
        except Exception as e:
            return make_response(jsonify({'message': 'An error occurred', 'error': str(e)}), 500)

    def post(self):
        
        beneficiary = Beneficiary(
            name=request.json['name'],
            recieved_amount=request.json['recieved_amount'],
            image_url=request.json['image_url'],
            organization_id=session['user_id']
        )
        db.session.add(beneficiary)
        db.session.commit()
        return make_response(jsonify({
            'id': beneficiary.id,
            'name': beneficiary.name,
            'recieved_amount': beneficiary.recieved_amount,
            'image_url': beneficiary.image_url,
            'organization_id': beneficiary.organization_id
        }), 200)


# EndPoints
api.add_resource(RegisterUser, '/register', endpoint='register_user')
api.add_resource(UserLogin, '/login', endpoint='login')
api.add_resource(OrganizationLogin, '/org/login', endpoint='organization_login')
api.add_resource(CheckSession, '/checksession', endpoint='checksession')  
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(AdminOrganizations, '/admin', endpoint='admin_organizations')
api.add_resource(AdminOrganizationByID, '/admin/<int:id>', endpoint='admin_organizations_by_id')
api.add_resource(SetUpOrganizationDetails, '/org/edit', endpoint='set_up_organization_details')
api.add_resource(OrganizationDashboard, '/organization', endpoint='organization_dashboard')
api.add_resource(RegisterOrganization, '/org/register', endpoint='register_organization')
api.add_resource(OrganizationDonations, '/organization/donations', endpoint='non_anonymous_donations')
api.add_resource(OrganizationCreateStories, '/createpost', endpoint='create_post')
api.add_resource(OrgCreateBeneficiary, '/beneficiary', endpoint='create_beneficiary')
api.add_resource(DonorOrganizations, '/donor/organization', endpoint='donor_organizations')
api.add_resource(DonorOrganizationByID, '/donor/organization/<int:id>', endpoint='donor_organization_by_id')
api.add_resource(Donate, '/donate', endpoint='donate')
api.add_resource(BeneficiariesStories, '/donor/stories', endpoint='beneficiaries_stories')

if __name__ == '__main__':
    app.run(port=5555, debug=True)