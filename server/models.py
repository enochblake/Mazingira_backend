from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    serialize_rules = ('-donations.user',)

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False, default='donor')  # Roles: 'donor', 'admin', 'org'

    donations = db.relationship('Donation', backref='user')
# Association proxy
    organizations = association_proxy('donations', 'organization', creator=lambda organization_obj: Donation(organization=organization_obj))
    stories = association_proxy('donations', 'story', creator=lambda story_obj: Donation(story=story_obj))
    
    def __repr__(self):
        return f'<User: Id: {self.id}, Name: {self.first_name} {self.last_name}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def authenticate(self, password):
        return check_password_hash(self.password_hash, password)
    
class Organization(db.Model, SerializerMixin):
    __tablename__ = 'organizations'
    serialize_rules = ('-donations.organization',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    image_url = db.Column(db.String, nullable=False)
    approval_status = db.Column(db.Boolean, default=False)
    description = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    password_hash = db.Column(db.String, nullable=False)

    donations = db.relationship('Donation', backref='organization')
    stories = db.relationship('Story', backref='organization')

    def __repr__(self):
        return f'<Organization: Id: {self.id}, Organization: {self.name} Details: {self.description}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def authenticate(self, password):
        return check_password_hash(self.password_hash, password)
    
class Donation(db.Model, SerializerMixin):
    __tablename__ = 'donations'
    serialize_rules = ('-donation.users', '-donation.organizations',)

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    anonymous = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    donor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))

    def __repr__(self):
        return f'<Donation: Id: {self.id}, Amount: {self.amount} Donated At:{self.created_at}>'

class Story(db.Model, SerializerMixin):
    __tablename__ = 'stories'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))

    def __repr__(self):
        return f'<Story: Id: {self.id}, Title: {self.title} Created At:{self.created_at}>'