from models import db, User, Organization, Donation, Story
from app import app

with app.app_context():

    User.query.delete()
    Organization.query.delete()
    Donation.query.delete()
    Story.query.delete()

    admin = User(email="admin@mazingira.com", first_name="Jay",last_name="Kimani", password_hash="admin", role="admin")
    donor = User(email="user@mazingira.com", first_name="Priscilla",last_name="Wakahia", password_hash="user")
    organization = Organization(name="Red Cross", image_url="werere", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ac nunc vel justo ullamcorper malesuada. Quisque euismod sapien sit amet nulla efficitur, sed sollicitudin dolor fringilla. Integer euismod turpis nec eros ultricies, sit amet tempus diam laoreet. Vivamus id felis auctor, aliquet ante ac, congue libero. Nulla facilisi. Phasellus nec nisi at libero facilisis condimentum. Sed vestibulum justo nec risus fermentum, id feugiat turpis convallis. Aenean nec mauris nec justo pharetra ultricies. Nullam nec neque sit amet mauris ultricies accumsan. Suspendisse potenti. Sed nec libero id est varius facilisis.")
    donation = Donation(amount=230, donor_id=1, organization_id=1)
    story = Story(title="Story 1", content="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ac nunc vel justo ullamcorper malesuada. Quisque euismod sapien sit amet nulla efficitur, sed sollicitudin dolor fringilla. Integer euismod turpis nec eros ultricies, sit amet tempus diam laoreet. Vivamus id felis auctor, aliquet ante ac, congue libero. Nulla facilisi. Phasellus nec nisi at libero facilisis condimentum. Sed vestibulum justo nec risus fermentum, id feugiat turpis convallis. Aenean nec mauris nec justo pharetra ultricies. Nullam nec neque sit amet mauris ultricies accumsan. Suspendisse potenti. Sed nec libero id est varius facilisis.", organization_id=1)

    db.session.add(admin)
    db.session.commit()
    db.session.add(donor)
    db.session.commit()
    print('Users Created')
    db.session.add(organization)
    db.session.commit()
    print('Organization Created')
    db.session.add(donation)
    db.session.commit()
    print('Donation Created')
    db.session.add(story)
    db.session.commit()
    print('Story Created')