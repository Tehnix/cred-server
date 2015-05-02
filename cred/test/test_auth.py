import unittest
import json
import cred
import cred.test.util


class AuthTestCase(cred.test.util.BaseTestCase):

    def test_POST_auth(self):
        # Use the helper function to authenticate with the server
        response = self.authenticate_with_server()
        # Decode the json response string into a python dictionary
        resp = json.loads(response.data.decode('utf-8'))
        # Check that we get the correct response
        self.assertEqual(response.status_code, 201)
        self.assertEqual(resp['status'], 201)
        self.assertEqual(resp['message'], 'Created')
        self.assertFalse(resp['scheduled']['assigned'])
        self.assertEqual(resp['scheduled']['slot'], None)
        self.assertEqual(resp['PINGTimeout'], 240)
        self.assertCountEqual(
            resp['subscribe'],
            list(cred.test.util.SUBSCRIBE.keys()))


if __name__ == '__main__':
    unittest.main()

