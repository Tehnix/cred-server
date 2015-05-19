import unittest
import json
import cred
import cred.test.util as testutil


class AuthTestCase(testutil.BaseTestCase):

    def test_client_can_authenticate(self):
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
            resp['scheduled']['assigned']: False
        })


if __name__ == '__main__':
    unittest.main()
