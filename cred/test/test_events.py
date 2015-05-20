import unittest
import json
import cred
import cred.test.util as testutil


test_event = {
    'event': {
        'name': 'Temperature',
        'location': 'Living Room',
        'action': 'Temperature Above Setting',
        'value': '5'
    }
}

subscribed_event = {
    'event': {
        'name': 'Light',
        'location': 'Living Room',
        'action': 'Light Changed',
        'value': 'On'
    }
}


class EventTestCase(testutil.BaseTestCase):

    @testutil.authenticate('write')
    def test_posting_a_complete_event(self):
        """Create a valid new event."""
        # Post the request to the test server
        response = self.client.post(
            '/events',
            data=json.dumps(test_event),
            content_type='application/json'
        )
        resp = json.loads(response.data.decode('utf-8'))
        # Check that we get the correct response
        testutil.assertEqual(self, {
            response.status_code: 201,
            resp['status']: 201,
            resp['message']: 'Created Event',
            'id' in resp['event']: True,
            'uri' in resp['event']: True
        })

    @testutil.authenticate('read')
    def test_cannot_create_an_event_when_read(self):
        """Test that you can't create an event with read permission."""
        # Post the request to the test server
        response = self.client.post(
            '/events',
            data=json.dumps(test_event),
            content_type='application/json'
        )
        resp = json.loads(response.data.decode('utf-8'))
        # Check that we get the correct response
        testutil.assertEqual(self, {
            response.status_code: 403,
            resp['status']: 403,
            resp['message']: 'Insufficient Permissions'
        })

    @testutil.authenticate('read')
    def test_access_events_when_none_are_created(self):
        """Fetch a list of events, when there are none."""
        response = self.client.get('/events')
        resp = json.loads(response.data.decode('utf-8'))
        # Check that we get the correct response
        testutil.assertEqual(self, {
            response.status_code: 200,
            resp['status']: 200,
            resp['message']: 'OK',
        })
        self.assertCountEqual(resp['events'], [])

    @testutil.authenticate('write')
    def test_getting_list_of_full_events(self):
        """Fetch a list of events with full information"""
        # Create a event that the client has subscribed to
        data = json.dumps(subscribed_event)
        self.client.post('/events', data=data, content_type='application/json')
        response = self.client.get('/events?full=true')
        resp = json.loads(response.data.decode('utf-8'))
        # Check that we actually get the full event in the feed
        testutil.assertEqual(self, {
            response.status_code: 200,
            resp['status']: 200,
            resp['message']: 'OK',
            resp['events'][0]['name']: 'Light',
            resp['events'][0]['location']: 'Living Room',
            resp['events'][0]['action']: 'Light Changed',
            resp['events'][0]['value']: 'On',
            'id' in resp['events'][0]: True,
            'uri' in resp['events'][0]: True,
            'time' in resp['events'][0]: True,
        })

    @testutil.authenticate('write')
    def test_getting_a_specific_event(self):
        """Fetch a specific event from an ID."""
        # Create an event, so we have something to request
        response = self.client.post(
            '/events',
            data=json.dumps(test_event),
            content_type='application/json'
        )
        event_resp = json.loads(response.data.decode('utf-8'))
        # Get the specific event
        response = self.client.get('/events/' + str(event_resp['event']['id']))
        resp = json.loads(response.data.decode('utf-8'))
        # Check that we get the correct response
        testutil.assertEqual(self, {
            response.status_code: 200,
            resp['status']: 200,
            resp['message']: 'OK',
            resp['event']['name']: test_event['event']['name'],
            resp['event']['device']: testutil.DEVICE,
            resp['event']['action']: test_event['event']['action'],
            resp['event']['value']: test_event['event']['value'],
            'id' in resp['event']: True,
            'uri' in resp['event']: True,
            'time' in resp['event']: True
        })

    @testutil.authenticate('read')
    def test_404_on_non_existant_event(self):
        """Try to fetch an event that doesn't exist."""
        response = self.client.get('/events/0')
        resp = json.loads(response.data.decode('utf-8'))
        # Check that we get the correct response
        testutil.assertEqual(self, {
            response.status_code: 404,
            resp['status']: 404,
            resp['message']: 'Event Not Found'
        })

    def test_denied_access_without_authentication(self):
        """Check for events without being authenticated."""
        response = self.client.get('/events')
        resp = json.loads(response.data.decode('utf-8'))
        # Check that we get the correct response
        testutil.assertEqual(self, {
            response.status_code: 401,
            resp['status']: 401,
            resp['message']: 'Not Authenticated'
        })


if __name__ == '__main__':
    unittest.main()
