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
        response = self.client.get('/clients/%s/events' % self.id)
        resp = json.loads(response.data.decode('utf-8'))
        # Check that we get the correct response
        testutil.assertEqual(self, {
            response.status_code: 200,
            resp['status']: 200,
            resp['message']: 'OK',
            d4['event']['id']: resp['events'][0]['id'],
            d3['event']['id']: resp['events'][1]['id'],
            d2['event']['id']: resp['events'][2]['id'],
        })

    @testutil.authenticate('read')
    def test_getting_list_of_clients_events_with_non_made(self):
        """Fetch a list of a clients events, when there are none."""
        # Create an event that the client is not subscribed to
        response = self.client.get('/clients/1/events')
        resp = json.loads(response.data.decode('utf-8'))
        # Check that we get the correct response
        testutil.assertEqual(self, {
            response.status_code: 200,
            resp['status']: 200,
            resp['message']: 'OK',
        })
        self.assertCountEqual(resp['events'], [])

    @testutil.authenticate('read')
    def test_getting_events_from_client_that_does_not_exist(self):
        """Test getting a list of events from a client that doesn't exist."""
        response = self.client.get('/clients/0/events')
        resp = json.loads(response.data.decode('utf-8'))
        testutil.assertEqual(self, {
            response.status_code: 404,
            resp['status']: 404,
            resp['message']: 'Client Not Found',
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
            '/clients/%s/subscribedevents' % self.id
        )
        resp = json.loads(response.data.decode('utf-8'))
        # Check that we get the correct response
        testutil.assertEqual(self, {
            response.status_code: 200,
            resp['status']: 200,
            resp['message']: 'OK',
            d4['event']['id']: resp['events'][0]['id'],
            d3['event']['id']: resp['events'][1]['id'],
            d2['event']['id']: resp['events'][2]['id'],
        })

    @testutil.authenticate('read')
    def test_getting_subscribedevents_from_client_that_does_not_exist(self):
        """
        Test getting a list of subscribedevents from a client that doesn't
        exist.

        """
        response = self.client.get('/clients/0/subscribedevents')
        resp = json.loads(response.data.decode('utf-8'))
        testutil.assertEqual(self, {
            response.status_code: 404,
            resp['status']: 404,
            resp['message']: 'Client Not Found',
        })

    @testutil.authenticate('read')
    def test_getting_list_of_clients_subscribed_events_with_non_made(self):
        """
        Fetch a list of a clients subscribed events, when there are none.

        """
        # Create an event that the client is not subscribed to
        response = self.client.get('/clients/1/subscribedevents')
        resp = json.loads(response.data.decode('utf-8'))
        # Check that we get the correct response
        testutil.assertEqual(self, {
            response.status_code: 200,
            resp['status']: 200,
            resp['message']: 'OK',
        })
        self.assertCountEqual(resp['events'], [])


if __name__ == '__main__':
    unittest.main()
