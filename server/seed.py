from models import db, User, Organization, Donation, Story
from app import app

with app.app_context():

    User.query.delete()
    Organization.query.delete()
    Donation.query.delete()
    Story.query.delete()

