import unittest
import json
import copy
import cred
import cred.test.util

test_event = {
    'event': {
        'device': cred.test.util.DEVICE,
        'name': 'Temperature',
        'location': 'Living Room',
        'action': 'Temperature Above Setting',
        'value': 5
    }
}

class EventTestCase(cred.test.util.BaseTestCase):

    def test_posting_a_complete_event(self):
        # Authenticate with the server
        self.authenticate_with_server()
        # Post the request to the test server
        response = self.app.post(
            '/event',
            data=json.dumps(test_event),
            content_type='application/json')
        resp = json.loads(response.data.decode('utf-8'))
        
        # Check that we get the correct response
        self.assertEqual(response.status_code, 201)
        self.assertEqual(resp['status'], 201)
        self.assertEqual(resp['message'], 'Created')
        self.assertTrue('id' in resp['event'])
        self.assertTrue(resp['event']['name'] in cred.test.util.EVENTS)
        self.assertEqual(resp['event']['name'], 'Temperature')
        self.assertEqual(resp['event']['device'], cred.test.util.DEVICE)
        self.assertEqual(resp['event']['action'], 'Temperature Above Setting')
        self.assertEqual(resp['event']['value'], '5')

    def test_getting_the_last_event(self):
        # Authenticate with the server
        self.authenticate_with_server()
        # Create an event, so we have something to request
        response = self.app.post(
            '/event',
            data=json.dumps(test_event),
            content_type='application/json')
        # Create another event, so we can check if we get the last event or the
        # first event
        test_event_last = copy.deepcopy(test_event)
        test_event_last['value'] = -5
        test_event_last['action'] = 'Temperature Below Setting'
        response = self.app.post(
            '/event',
            data=json.dumps(test_event_last),
            content_type='application/json')
        event_post_resp = json.loads(response.data.decode('utf-8'))

        # Get the latest event from the server
        response = self.app.get('/event')
        resp = json.loads(response.data.decode('utf-8'))

        # Check that we get the correct response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp['status'], 200)
        self.assertEqual(resp['message'], 'OK')
        self.assertTrue('id' in resp['event'])
        self.assertEqual(resp['event']['name'], event_post_resp['event']['name'])
        self.assertEqual(resp['event']['device'], event_post_resp['event']['device'])
        self.assertEqual(resp['event']['action'], event_post_resp['event']['action'])
        self.assertEqual(resp['event']['value'], event_post_resp['event']['value'])

    def test_getting_a_specific_event(self):
        # Authenticate with the server
        self.authenticate_with_server()
        # Create an event, so we have something to request
        response = self.app.post(
            '/event',
            data=json.dumps(test_event),
            content_type='application/json')
        event_post_resp = json.loads(response.data.decode('utf-8'))

        # Get the latest event from the server
        response = self.app.get('/event/' + str(event_post_resp['event']['id']))
        resp = json.loads(response.data.decode('utf-8'))

        # Check that we get the correct response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp['status'], 200)
        self.assertEqual(resp['message'], 'OK')
        self.assertTrue('id' in resp['event'])
        self.assertEqual(resp['event']['name'], event_post_resp['event']['name'])
        self.assertEqual(resp['event']['device'], event_post_resp['event']['device'])
        self.assertEqual(resp['event']['action'], event_post_resp['event']['action'])
        self.assertEqual(resp['event']['value'], event_post_resp['event']['value'])


if __name__ == '__main__':
    unittest.main()

