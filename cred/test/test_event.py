import unittest
import json
import cred
import cred.test.util as testutil


test_event = {
    'event': {
        'device': testutil.DEVICE,
        'name': 'Temperature',
        'location': 'Living Room',
        'action': 'Temperature Above Setting',
        'value': '5'
    }
}

subscribed_event = {
    'event': {
        'device': 'Lamp',
        'name': 'Light',
        'location': 'Living Room',
        'action': 'Light Changed',
        'value': 'On'
    }
}

not_subscribed_event = {
    'event': {
        'device': 'Lamp',
        'name': 'Light',
        'location': 'Living Room',
        'action': 'Light Changed',
        'value': 'On'
    }
}


class EventTestCase(testutil.BaseTestCase):

    @testutil.authenticate
    def test_posting_a_complete_event(self):
        """Create a complete new event."""
        # Post the request to the test server
        response = self.app.post(
            '/events',
            data=json.dumps(test_event),
            content_type='application/json'
        )
        resp = json.loads(response.data.decode('utf-8'))

        # Check that we get the correct response
        testutil.assertEqual(self, {
            response.status_code: 201,
            resp['status']: 201,
            resp['message']: 'Created',
            resp['event']['name']: 'Temperature',
            resp['event']['device']: testutil.DEVICE,
            resp['event']['action']: 'Temperature Above Setting',
            resp['event']['value']: '5',
            'id' in resp['event']: True,
            resp['event']['name'] in testutil.EVENTS: True
        })

    @testutil.authenticate
    def test_access_events_when_none_are_created(self):
        """Fetch a list of new events, when there are no new ones yet."""
        response = self.app.get('/events')
        resp = json.loads(response.data.decode('utf-8'))
        # Check that we get the correct response
        testutil.assertEqual(self, {
            response.status_code: 200,
            resp['status']: 200,
            resp['message']: 'OK',
            resp['newEvents']: False
        })
        self.assertCountEqual(resp['events'], {})

    @testutil.authenticate
    def test_getting_list_of_new_events(self):
        """Fetch a list of new events, when there are new events waiting."""
        # Create an event that the client is not subscribed to
        r = self.app.post(
            '/events',
            data=json.dumps(not_subscribed_event),
            content_type='application/json'
        )
        d1 = json.loads(r.data.decode('utf-8'))
        # Create some events in the database that the client is subscribed to
        data = json.dumps(subscribed_event)
        r = self.app.post('/events', data=data, content_type='application/json')
        d2 = json.loads(r.data.decode('utf-8'))
        r = self.app.post('/events', data=data, content_type='application/json')
        d3 = json.loads(r.data.decode('utf-8'))
        r = self.app.post('/events', data=data, content_type='application/json')
        d4 = json.loads(r.data.decode('utf-8'))
        # Check the server for new events
        response = self.app.get('/events')
        resp = json.loads(response.data.decode('utf-8'))

        # Check that we get the correct response
        testutil.assertEqual(self, {
            response.status_code: 200,
            resp['status']: 200,
            resp['message']: 'OK',
            resp['newEvents']: True,
            d1['event']['id'] not in resp['events']: True,
            d2['event']['id'] in resp['events']: True,
            d3['event']['id'] in resp['events']: True,
            d4['event']['id'] in resp['events']: True
        })

    @testutil.authenticate
    def test_getting_a_specific_event(self):
        """Fetch a specific event from an ID."""
        # Create an event, so we have something to request
        response = self.app.post(
            '/events',
            data=json.dumps(test_event),
            content_type='application/json'
        )
        event_resp = json.loads(response.data.decode('utf-8'))
        # Get the specific event
        response = self.app.get('/events/' + str(event_resp['event']['id']))
        resp = json.loads(response.data.decode('utf-8'))
        # Check that we get the correct response
        testutil.assertEqual(self, {
            response.status_code: 200,
            resp['status']: 200,
            resp['message']: 'OK',
            resp['event']['name']: event_resp['event']['name'],
            resp['event']['device']: event_resp['event']['device'],
            resp['event']['action']: event_resp['event']['action'],
            resp['event']['value']: event_resp['event']['value'],
            'id' in resp['event']: True
        })

    @testutil.authenticate
    def test_404_on_non_existant_event(self):
        """Try to fetch an event that doesn't exist."""
        response = self.app.get('/events/0')
        resp = json.loads(response.data.decode('utf-8'))
        # Check that we get the correct response
        testutil.assertEqual(self, {
            response.status_code: 404,
            resp['status']: 404,
            resp['message']: 'Not Found'
        })

    def test_denied_access_without_authentication(self):
        """Check for new events without being authenticated."""
        response = self.app.get('/events')
        resp = json.loads(response.data.decode('utf-8'))
        # Check that we get the correct response
        testutil.assertEqual(self, {
            response.status_code: 401,
            resp['status']: 401,
            resp['message']: 'Unauthorized'
        })


if __name__ == '__main__':
    unittest.main()
