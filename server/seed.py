import random

from models import db, User, Organization, Donation, Story, Beneficiary
from app import app
from faker import Faker

fake = Faker()

history = "Founded in 2000 by Dr. Emily Carter, aims to combat soil pollution through research, public education, and sustainable land management practices. The organization has conducted groundbreaking studies, launched awareness campaigns, and developed educational programs for schools. By partnering with international bodies like UNEP and FAO, SoilGuard has expanded its reach and influence globally. Recent initiatives include the use of phytoremediation technologies and community-driven soil conservation projects. SoilGuard continues to be a leader in advocating for soil health and environmental sustainability."
categories = ['air', 'soil', 'water']
approval_status = [True, False]

with app.app_context():

    # Delete All Rows To Work On A Clean Slate
    # Donation.query.delete()
    # print('Deleted Donations')
    # Beneficiary.query.delete()
    # print('Deleted Beneficiaries')
    # Story.query.delete()
    # print('Deleted Stories')
    # Organization.query.delete()
    # print('Deleted Organizations')
    # User.query.delete()
    # print('Deleted Users')

    # # Populate User Table

    # for x in range(30):
    #     donor = User(email=fake.ascii_free_email(), first_name=fake.first_name(), last_name=fake.last_name())
    #     donor.set_password(fake.name())
    #     db.session.add(donor)
    #     db.session.commit
    # print('Donors Created')

    # admin = User(email="admin@mazingira.com", first_name="Jay",last_name="Kimani", role="admin")
    # admin.set_password('admin')
    # db.session.add(admin)
    # db.session.commit()
    # print('Admin Created')

    # # Populate Organization Table

    # for x in range(20):
    #     organization = Organization(name=fake.company(),approval_status=random.choice(approval_status) , email=fake.company_email(), category=random.choice(categories), description=fake.sentence(nb_words=5), history=history, image_url='https://thumbs.dreamstime.com/b/hands-child-holding-young-plants-back-soil-nature-park-growth-plant-hands-child-holding-young-plants-111399665.jpg')
    #     organization.set_password(fake.name())
    #     db.session.add(organization)
    #     db.session.commit()
    # print('Organizations Created')

    # Populate Donation Table

    # for x in range(200):
    #     donation = Donation(amount=fake.random_int(min=500, max=10000), donor_id=fake.random_int(min=1, max=30), anonymous=random.choice(approval_status), organization_id=fake.random_int(min=1, max=20))
    #     db.session.add(donation)
    #     db.session.commit()
    # print('Donation Created')

    # Populate Beneficiaries Table

    # for x in range(100):
    #     beneficiaries = Beneficiary(name=fake.name(), recieved_amount=fake.random_int(min=300, max=1000), image_url="https://pbs.twimg.com/media/FpmD9sMXEAA4Mb7.jpg", organization_id=fake.random_int(min=1, max=20) )
    #     db.session.add(beneficiaries)
    #     db.session.commit()
    # print('Beneficiaries Created')

    # https://i.pinimg.com/originals/63/f9/d5/63f9d5fd5f34c8544a31c22c3e909cec.jpg

    # Populate Story Table

    # for x in range(40):
    #     story = Story(title=fake.name(), content=fake.paragraph(nb_sentences=8),image_url="https://i.pinimg.com/originals/63/f9/d5/63f9d5fd5f34c8544a31c22c3e909cec.jpg", organization_id=21, beneficiary_id=fake.random_int(min=101, max=150))
    #     db.session.add(story)
    #     db.session.commit()
    # print('Stories Created')

    print('Completed!!')
