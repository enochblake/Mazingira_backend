from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Organization
# from flask_bcrypt import Bcrypt


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)
# bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return '<h1>Welcome To Mazingira</h1>'

class AdminDashboard(Resource):
    # def get(self):
    #     organizations = Organization.query.all()
    #     print(organizations)
    #     resp = make_response({
    #         'project': 'Flask RESTful API',
    #         'authors': 'John Kimani M. & Priscilla M. Wakahia'
    #     }, 200)
    #     return resp
    def get(self):
        try:
            organizations = []
            for organization in Organization.query.all():
                organizations.append({
                    'id': organization.id,
                    'name': organization.name,
                    'image_url': organization.image_url,
                    'approval_status': organization.approval_status,
                    'description': organization.description,
                })
            if organizations:
                return make_response(jsonify({'message': 'success', 'data': organizations}), 200)
            else:
                return make_response(jsonify({'message': 'No Organizations Found'}), 404)
        except Exception as e:
            return make_response(jsonify({'message': 'An error occurred', 'error': str(e)}), 500)
    
    def post(self):
        pass

    def patch(self):
        pass

    def delete(self,id):
        organization = Organization.query.get(id)
        organization.query.delete()
        return f"Deletion Successful"

# EndPoints
api.add_resource(AdminDashboard, '/admin', endpoint='home') 


if __name__ == '__main__':
    app.run(port=5555, debug=True)