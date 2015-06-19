import unittest
import json
import cred
import cred.test.util as testutil


class AuthTestCase(testutil.BaseTestCase):

    def test_client_can_authenticate(self):
        """Authenticate a client."""
        # Use the helper function to authenticate with the server
        response = self.authenticate_with_server('read')
        # Decode the json response string into a python dictionary
        resp = json.loads(response.data.decode('utf-8'))
        # Check that we get the correct response
        testutil.assertEqual(self, {
            response.status_code: 201,
            resp['status']: 201,
            resp['message']: 'Authenticated',
            'id' in resp: True,
            'sessionKey' in resp: True,
            resp['scheduled']['slot']: None,
            resp['PINGTimeout']: 240,
            resp['scheduled']['assigned']: False,
            resp['scheduled']['period']: None
        })

    def test_that_apikey_is_required(self):
        """Test that an API key is required for authentication."""
        test_auth = {
            'device': 'Thermostat',
            'location': 'Living Room',
            'subscribe': {}
        }
        response = self.client.post(
            '/auth',
            data=json.dumps(test_auth),
            content_type='application/json'
        )
        print(response.data)
        resp = json.loads(response.data.decode('utf-8'))
        # Check that we get the correct response
        testutil.assertEqual(self, {
            response.status_code: 401,
            resp['status']: 401,
            resp['message']: 'Invalid API Key'
        })


if __name__ == '__main__':
    unittest.main()
