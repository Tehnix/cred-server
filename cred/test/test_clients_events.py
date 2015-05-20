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

not_subscribed_event = {
    'event': {
        'name': 'Light',
        'location': 'Lobby',
        'action': 'Light Changed',
        'value': 'On'
    }
}


class ClientsEventsTestCase(testutil.BaseTestCase):

    @testutil.authenticate('write')
    def test_getting_list_of_clients_events(self):
        """Fetch a list of a clients events."""
        # Create some events in the database
        data = json.dumps(subscribed_event)
        r = self.client.post(
            '/events',
            data=data,
            content_type='application/json'
        )
        d2 = json.loads(r.data.decode('utf-8'))
        r = self.client.post(
            '/events',
            data=data,
            content_type='application/json'
        )
        d3 = json.loads(r.data.decode('utf-8'))
        r = self.client.post(
            '/events',
            data=data,
            content_type='application/json'
        )
        d4 = json.loads(r.data.decode('utf-8'))
        # Check the server for new events
        response = self.client.get('/clients/%s/events' % self.client_id)
        resp = json.loads(response.data.decode('utf-8'))
        print(resp)
        # Check that we get the correct response
        testutil.assertEqual(self, {
            response.status_code: 200,
            resp['status']: 200,
            resp['message']: 'OK',
            d2['event']['id']: resp['events'][0]['id'],
            d3['event']['id']: resp['events'][1]['id'],
            d4['event']['id']: resp['events'][2]['id'],
        })

    @testutil.authenticate('write')
    def test_getting_list_of_clients_subscribed_events(self):
        """Fetch a list of a clients subscribed events."""
        # Create an event that the client is not subscribed to
        r = self.client.post(
            '/events',
            data=json.dumps(not_subscribed_event),
            content_type='application/json'
        )
        d1 = json.loads(r.data.decode('utf-8'))
        # Create some events in the database that the client is subscribed to
        data = json.dumps(subscribed_event)
        r = self.client.post(
            '/events',
            data=data,
            content_type='application/json'
        )
        d2 = json.loads(r.data.decode('utf-8'))
        r = self.client.post(
            '/events',
            data=data,
            content_type='application/json'
        )
        d3 = json.loads(r.data.decode('utf-8'))
        r = self.client.post(
            '/events',
            data=data,
            content_type='application/json'
        )
        d4 = json.loads(r.data.decode('utf-8'))
        # Check the server for new events
        response = self.client.get(
            '/clients/%s/subscribedevents' % self.client_id
        )
        resp = json.loads(response.data.decode('utf-8'))
        # Check that we get the correct response
        testutil.assertEqual(self, {
            response.status_code: 200,
            resp['status']: 200,
            resp['message']: 'OK',
            d2['event']['id']: resp['events'][0]['id'],
            d3['event']['id']: resp['events'][1]['id'],
            d4['event']['id']: resp['events'][2]['id'],
        })


if __name__ == '__main__':
    unittest.main()
