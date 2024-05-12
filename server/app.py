from flask import Flask, make_response, jsonify, request, session
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
                user_dict = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'role': user.role,
                }
                return make_response(user_dict, 200)
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
            resp = {'message': f'Congratulations {first_name} {last_name}! Successfully Registered'}
            return make_response(resp, 201)
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
            resp = {'message': f'Congratulations {name}! Successfully Registered'}
            return make_response(resp, 201)
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
                org_dict = {
                'id': org.id,
                'name': org.name,
                'approval_status': org.approval_status,
                'email': org.email,
                'description': org.description,
                'image_url': org.image_url,
                'registered_on': org.created_at,
                'application_reviewed_on': org.updated_at
                }
                return make_response(org_dict, 200)
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
                'image_url': org.image_url,
                'registered_on': org.created_at,
                'application_reviewed_on': org.updated_at
                }
            return make_response(org_dict, 200)
        else:
            return {'message': '401: Not Authorized'}, 401
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
                    'created_at': story.created_at,
                    'organization_id': story.organization_id,
                })
            if stories:
                return make_response(jsonify({'message': 'success', 'data': stories}), 200)
            else:
                return make_response(jsonify({'message': 'No Stories Found. Make A Donation First'}), 404)
        except Exception as e:
            return make_response(jsonify({'message': 'An error occurred', 'error': str(e)}), 500)


# Organizations Endpoints

class OrganizationDashboard(Resource):
    
    def get(self):
        pass

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
            'description': organization.description,
        }}, 200

class OrganizationNonAnonymousDonations(Resource):
    
    def get(self):
        try:
            donations = []
            for donation in Donation.query.filter_by(anonymous = False).all():
                donations.append({
                    'id': donation.id,
                    'amount': donation.amount,
                    'created_at': donation.created_at,
                    'donor_id': donation.donor_id,
                    'organization_id': donation.organization_id,
                    
                })
            if donations:
                return make_response(jsonify({'message': 'success', 'data': donations}), 200)
            else:
                return make_response(jsonify({'message': 'No Organizations Found'}), 404)
        except Exception as e:
            return make_response(jsonify({'message': 'An error occurred', 'error': str(e)}), 500)
        
class OrganizationCreateStories(Resource):

    def post(self):
        
        story = Story(
            title=request.json['title'],
            content=request.json['title'],
            image_url=request.json['title'],
            organization_id=session['user_id']
        )
        db.session.add(story)
        db.session.commit()
        return make_response(jsonify({
            'id': story.id,
            'title': story.title,
            'content': story.content,
            'image_url': story.image_url,
            'organization_id': story.organization_id,
            'created_at': story.created_at
        }), 200)




# EndPoints
api.add_resource(RegisterUser, '/register', endpoint='register_user')
api.add_resource(UserLogin, '/login', endpoint='login')
api.add_resource(OrganizationLogin, '/org/login', endpoint='organization_login')
api.add_resource(CheckSession, '/check_session', endpoint='checksession')  
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(AdminOrganizations, '/admin', endpoint='admin_organizations')
api.add_resource(AdminOrganizationByID, '/admin/<int:id>', endpoint='admin_organizations_by_id')
api.add_resource(SetUpOrganizationDetails, '/org/edit', endpoint='set_up_organization_details')
api.add_resource(OrganizationDashboard, '/organization', endpoint='organization_dashboard')
api.add_resource(RegisterOrganization, '/org/register', endpoint='register_organization')
api.add_resource(OrganizationNonAnonymousDonations, '/organization/donations', endpoint='non_anonymous_donations')
api.add_resource(OrganizationCreateStories, '/org/createpost', endpoint='create_post')
api.add_resource(DonorOrganizations, '/donor/organization', endpoint='donor_organizations')
api.add_resource(DonorOrganizationByID, '/donor/organization/<int:id>', endpoint='donor_organization_by_id')
api.add_resource(Donate, '/donate', endpoint='donate')
api.add_resource(BeneficiariesStories, '/donor/stories', endpoint='beneficiaries_stories')

if __name__ == '__main__':
    app.run(port=5555, debug=True)