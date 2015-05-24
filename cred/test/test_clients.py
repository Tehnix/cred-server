import unittest
import json
import cred
import cred.test.util as testutil


class ClientsTestCase(testutil.BaseTestCase):

    def test_getting_a_list_of_clients(self):
        """Test getting a list of clients."""
        # Create different clients, by authenticating with them
        self.authenticate_with_server('read', alternate_device='Alarm')
        self.authenticate_with_server('read', alternate_device='Light')
        self.authenticate_with_server('read', alternate_device='Thermostat')
        response = self.client.get('/clients')
        resp = json.loads(response.data.decode('utf-8'))
        testutil.assertEqual(self, {
            response.status_code: 200,
            resp['status']: 200,
            resp['message']: 'OK',
            'device' not in resp['clients'][0]: True,
            'location' not in resp['clients'][0]: True,
            'id' in resp['clients'][0]: True,
            'uri' in resp['clients'][0]: True,
        })

    def test_getting_a_list_of_clients_with_full_information(self):
        """Test getting a list of clients with full information."""
        # Create different clients, by authenticating with them
        self.authenticate_with_server('read', alternate_device='Alarm')
        self.authenticate_with_server('read', alternate_device='Light')
        self.authenticate_with_server('read', alternate_device='Thermostat')
        response = self.client.get('/clients?full=true')
        resp = json.loads(response.data.decode('utf-8'))
        testutil.assertEqual(self, {
            response.status_code: 200,
            resp['status']: 200,
            resp['message']: 'OK',
            resp['clients'][2]['device']: 'Alarm',
            resp['clients'][2]['location']: 'Living Room',
            'id' in resp['clients'][0]: True,
            'uri' in resp['clients'][0]: True,
        })

    def test_getting_the_client_itself(self):
        """Test getting the client's own information"""
        # Create different clients, by authenticating with them
        self.authenticate_with_server('read', alternate_device='Alarm')
        self.authenticate_with_server('read', alternate_device='Light')
        self.authenticate_with_server('read', alternate_device='Thermostat')
        response = self.client.get('/clients/me')
        resp = json.loads(response.data.decode('utf-8'))
        testutil.assertEqual(self, {
            response.status_code: 200,
            resp['status']: 200,
            resp['message']: 'OK',
            resp['client']['device']: 'Thermostat',
            resp['client']['location']: 'Living Room',
            'id' in resp['client']: True,
            'uri' in resp['client']: True,
        })

    def test_getting_a_client_by_id(self):
        """Test getting a specific client."""
        # Create different clients, by authenticating with them
        self.authenticate_with_server('read', alternate_device='Alarm')
        client2 = self.authenticate_with_server('read', alternate_device='Light')
        self.authenticate_with_server('read', alternate_device='Thermostat')
        client2_resp = json.loads(client2.data.decode('utf-8'))
        response = self.client.get('/clients/' + str(client2_resp['id']))
        resp = json.loads(response.data.decode('utf-8'))
        testutil.assertEqual(self, {
            response.status_code: 200,
            resp['status']: 200,
            resp['message']: 'OK',
            resp['client']['device']: 'Light',
            resp['client']['location']: 'Living Room',
            'id' in resp['client']: True,
            'uri' in resp['client']: True,
        })

    @testutil.authenticate('read')
    def test_getting_a_client_by_id_that_does_not_exist(self):
        """Test getting a client that doesn't exist."""
        response = self.client.get('/clients/0')
        resp = json.loads(response.data.decode('utf-8'))
        testutil.assertEqual(self, {
            response.status_code: 404,
            resp['status']: 404,
            resp['message']: 'Client Not Found',
        })


if __name__ == '__main__':
    unittest.main()
