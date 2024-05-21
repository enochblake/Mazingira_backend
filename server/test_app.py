import unittest
from app import app, db, Payment
from flask import json

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_payments.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_payment(self):
        response = self.app.post('/paypal', json={'amount': 10.00})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('payment_id', data)
        self.assertIn('approval_url', data)

    def test_execute_payment(self):
        # Create a payment first
        response = self.app.post('/paypal', json={'amount': 10.00})
        data = json.loads(response.data)
        payment_id = data['payment_id']
        
        # Mock a payment execution
        response = self.app.post('/paypal/execute', json={
            'payment_id': payment_id,
            'payer_id': 'TESTPAYERID'
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Payment executed successfully')

        payment = Payment.query.filter_by(payment_id=payment_id).first()
        self.assertIsNotNone(payment)
        self.assertEqual(payment.payer_id, 'TESTPAYERID')
        self.assertEqual(payment.status, 'approved')

if __name__ == '__main__':
    unittest.main()
