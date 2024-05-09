from models import db, User, Organization, Donation, Story
from app import app
from faker import Faker

fake = Faker()

with app.app_context():

    # Delete All Rows To Work On A Clean Slate
    User.query.delete()
    Organization.query.delete()
    Donation.query.delete()
    Story.query.delete()

    # Populate User Table

    for x in range(30):
        donor = User(email=fake.ascii_free_email(), first_name=fake.first_name(), last_name=fake.last_name(), password_hash=fake.name())
        db.session.add(donor)
        db.session.commit
    print('Donors Created')

    # Populate Organization Table

    for x in range(10):
        organization = Organization(name=fake.company(), email=fake.company_email(), image_url="https://cleanmanagement.com/wp-content/uploads/2023/10/CleanManagementEnvironmentalGroup-252418-Environmental-Protection-Agency-blogbanner1.jpg", description=fake.paragraph(nb_sentences=4), password_hash=fake.name())
        db.session.add(organization)
        db.session.commit()
    print('Organization Created')

    admin = User(email="admin@mazingira.com", first_name="Jay",last_name="Kimani", password_hash="admin", role="admin")
    db.session.add(admin)
    db.session.commit()

    # Populate Donation Table

    for x in range(50):
        donation = Donation(amount=fake.random_int(min=500, max=10000), donor_id=fake.random_int(min=1, max=30), organization_id=fake.random_int(min=1, max=10))
        db.session.add(donation)
        db.session.commit()
    print('Donation Created')

    # Populate Story Table
    for x in range(40):
        story = Story(title=fake.name(), content=fake.paragraph(nb_sentences=6),image_url="https://pbs.twimg.com/media/FpmD9sMXEAA4Mb7.jpg", organization_id=fake.random_int(min=1, max=10))
        db.session.add(story)
        db.session.commit()
    print('Story Created')