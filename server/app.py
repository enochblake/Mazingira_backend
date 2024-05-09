from flask import Flask, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Organization
# , User, Donation, Story
# from flask_bcrypt import Bcrypt

app = Flask(__name__)
CORS(app)


app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
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

class AdminDashboard(Resource):
    def get(self):
        resp = make_response({
            'project': 'Mazingira',
            'authors': 'John, Enoch, Charity, Priscilla, Dennis'
        }, 200)
        # print(Organization.query.one())
        return resp
    # View All food as the Admin and perform all CRUD operations
    # def get(self):
    #     orgs_list = [{
    #         'id': organization.id,
    #         'name': organization.name,
    #         'image_url': organization.image_url,
    #         'approval_status': organization.approval_status,
    #         'description': organization.description,
    #     } for organization in Organization.query.all()]
    #     return make_response(jsonify(orgs_list), 200)
    def get(self):
        try:
            orgs = []
            for organization in Organization.query.all():
                orgs.append({
                    'id': organization.id,
                    'name': organization.name,
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
    
    def post(self):
        pass

    def patch(self):
        pass

    # def delete(self,id):
    #     organization = organization = Organization.query.filter_by(id=id).first()
    #     organization.query.delete()
    #     return f"Deletion Successful"

    def delete(self, id):
        organization = Organization.query.get(id)
        if organization:
            db.session.delete(organization)
            db.session.commit()
            return {'message': 'Organization deleted successfully'}, 200
        else:
            return {'message': 'Organization not found'}, 404

# EndPoints
api.add_resource(AdminDashboard, '/admin', endpoint='admin')
# api.add_resource(AdminDashboard, '/admin/<int:id>', endpoint='admin')


if __name__ == '__main__':
    app.run(port=5555, debug=True)