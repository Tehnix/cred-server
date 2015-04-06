import os
import unittest
import tempfile
import json
import cred

APIKey = 'uJidciTE1fuJXf37gs8MgPskMjYLxe'

class RunserverTestCase(unittest.TestCase):
    def setUp(self):
        self.dbFD, self.dbfile = tempfile.mkstemp()
        cred.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        cred.app.config['SQLALCHEMY_DATABASE_URI'] += self.dbfile
        cred.app.config['TESTING'] = True
        self.app = cred.app.test_client()
        cred.initDB()

    def tearDown(self):
        os.close(self.dbFD)
        os.unlink(self.dbfile)

    def testPOSTAuth(self):
        req = json.dumps({
            'apiKey': APIKey,
            'device': 'Thermostat',
            'location': 'Living Rooom',
            'events': ['Temperature'],
            'subscribes': {
                'Light': {'location': 'Living Room'},
                'Alarm': {}
            }
        })
        response = self.app.post(
            '/auth',
            data=req,
            content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, json.dumps({
            'status': 'created',
            'scheduled': {
                'assigned': False,
                'slot': None
            },
            'PINGTimeout': 240
        }).encode('utf-8'))

    def testPOSTEvent(self):
        req = json.dumps({
            'apiKey': APIKey,
            'event': {
                'location': 'Living Room',
                'action': 'Temperature Above Setting',
                'value': 5
            }
        })
        response = self.app.post(
            '/event',
            data=req,
            content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, json.dumps({
            'status': 'created',
            'event': {
                #'name': 'Temperature',
                #'device': 'Thermostat',
                'action': 'Temperature Above Setting',
                'value': '5'
            }
        }).encode('utf-8'))

if __name__ == '__main__':
    unittest.main()

