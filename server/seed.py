from models import db, User, Organization, Donation, Story, Beneficiary
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
        donor = User(email=fake.ascii_free_email(), first_name=fake.first_name(), last_name=fake.last_name())
        donor.set_password(fake.name())
        db.session.add(donor)
        db.session.commit
    print('Donors Created')

    admin = User(email="admin@mazingira.com", first_name="Jay",last_name="Kimani", role="admin")
    admin.set_password('admin')
    db.session.add(admin)
    db.session.commit()
    print('Admin Created')

    # Populate Organization Table

    for x in range(10):
        organization = Organization(name=fake.company(), email=fake.company_email())
        organization.set_password(fake.name())
        db.session.add(organization)
        db.session.commit()
    print('Organizations Created')

    organization = Organization(name='Just An Organization', email='org@mazingira.com',)
    organization.set_password('password')
    db.session.add(organization)
    db.session.commit()
    print('Organization Created')


    # Populate Donation Table

    for x in range(50):
        donation = Donation(amount=fake.random_int(min=500, max=10000), donor_id=fake.random_int(min=1, max=30), organization_id=fake.random_int(min=1, max=10))
        db.session.add(donation)
        db.session.commit()
    print('Donation Created')

    # Populate Beneficiaries Table

    for x in range(70):
        beneficiaries = Beneficiary(name=fake.name(), recieved_amount=fake.random_int(min=500, max=1000), image_url="https://pbs.twimg.com/media/FpmD9sMXEAA4Mb7.jpg", organization_id=fake.random_int(min=1, max=10) )
        db.session.add(beneficiaries)
        db.session.commit()
    print('Beneficiaries Created')

    # Populate Story Table
    for x in range(40):
        story = Story(title=fake.name(), content=fake.paragraph(nb_sentences=6),image_url="https://pbs.twimg.com/media/FpmD9sMXEAA4Mb7.jpg", organization_id=fake.random_int(min=1, max=10), beneficiary_id=fake.random_int(min=1, max=10))
        db.session.add(story)
        db.session.commit()
    print('Stories Created')