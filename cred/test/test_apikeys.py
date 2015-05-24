import unittest
import json
import cred
import cred.test.util as testutil


class APIKeyTestCase(testutil.BaseTestCase):

    @testutil.authenticate('admin')
    def test_creating_apikey(self):
        """Create an API key."""
        # Post the request to the test server
        response = self.client.post(
            '/apikeys',
            data=json.dumps({'permission': 'write'}),
            content_type='application/json'
        )
        resp = json.loads(response.data.decode('utf-8'))
        # Check that we get the correct response
        testutil.assertEqual(self, {
            response.status_code: 201,
            resp['status']: 201,
            resp['message']: 'Created API Key',
            resp['apikey']['permission']: 'write',
            'id' in resp['apikey']: True,
            'apikey' in resp['apikey']: True,
            'created' in resp['apikey']: True,
            'uri' in resp['apikey']: True
        })

    @testutil.authenticate('admin')
    def test_creating_apikey_with_invalid_permissions(self):
        """Cannot create an API key with invalid permissions."""
        # Post the request to the test server
        response = self.client.post(
            '/apikeys',
            data=json.dumps({'permission': 'this is invalid'}),
            content_type='application/json'
        )
        resp = json.loads(response.data.decode('utf-8'))
        # Check that we get the correct response
        testutil.assertEqual(self, {
            response.status_code: 400,
            resp['status']: 400,
            resp['message']: 'Invalid Permissions',
        })

    @testutil.authenticate('read')
    def test_cannot_create_apikey_when_read(self):
        """Test that you can't create an api key with read permissions."""
        # Post the request to the test server
        response = self.client.post(
            '/apikeys',
            data=json.dumps({'permission': 'write'}),
            content_type='application/json'
        )
        resp = json.loads(response.data.decode('utf-8'))
        # Check that we get the correct response
        testutil.assertEqual(self, {
            response.status_code: 403,
            resp['status']: 403,
            resp['message']: 'Insufficient Permissions',
        })

    @testutil.authenticate('write')
    def test_cannot_create_apikey_when_write(self):
        """Test that you can't create an api key with write permissions."""
        # Post the request to the test server
        response = self.client.post(
            '/apikeys',
            data=json.dumps({'permission': 'write'}),
            content_type='application/json'
        )
        resp = json.loads(response.data.decode('utf-8'))
        # Check that we get the correct response
        testutil.assertEqual(self, {
            response.status_code: 403,
            resp['status']: 403,
            resp['message']: 'Insufficient Permissions',
        })

    @testutil.authenticate('admin')
    def test_getting_a_list_of_apikeys(self):
        """Get a list of API keys."""
        response = self.client.post(
            '/apikeys',
            data=json.dumps({'permission': 'write'}),
            content_type='application/json'
        )
        a1 = json.loads(response.data.decode('utf-8'))
        response = self.client.post(
            '/apikeys',
            data=json.dumps({'permission': 'write'}),
            content_type='application/json'
        )
        a2 = json.loads(response.data.decode('utf-8'))
        response = self.client.post(
            '/apikeys',
            data=json.dumps({'permission': 'write'}),
            content_type='application/json'
        )
        a3 = json.loads(response.data.decode('utf-8'))
        response = self.client.get('/apikeys')
        resp = json.loads(response.data.decode('utf-8'))
        testutil.assertEqual(self, {
            response.status_code: 200,
            resp['status']: 200,
            resp['message']: 'OK',
            a3['apikey']['id']: resp['apikeys'][0]['id'],
            a2['apikey']['id']: resp['apikeys'][1]['id'],
            a1['apikey']['id']: resp['apikeys'][2]['id'],
        })

    @testutil.authenticate('read')
    def test_cannot_get_a_list_of_apikeys_when_read(self):
        """Test that you can't fetch api keys with read permissions."""
        response = self.client.get('/apikeys')
        resp = json.loads(response.data.decode('utf-8'))
        # Check that we get the correct response
        testutil.assertEqual(self, {
            response.status_code: 403,
            resp['status']: 403,
            resp['message']: 'Insufficient Permissions',
        })

    @testutil.authenticate('write')
    def test_cannot_get_a_list_of_apikeys_when_write(self):
        """Test that you can't fetch api keys with write permissions."""
        response = self.client.get('/apikeys')
        resp = json.loads(response.data.decode('utf-8'))
        # Check that we get the correct response
        testutil.assertEqual(self, {
            response.status_code: 403,
            resp['status']: 403,
            resp['message']: 'Insufficient Permissions',
        })

    @testutil.authenticate('admin')
    def test_getting_a_specific_apikey(self):
        """Get a specific API key from ID."""
        response = self.client.get('/apikeys/1')
        resp = json.loads(response.data.decode('utf-8'))
        testutil.assertEqual(self, {
            response.status_code: 200,
            resp['status']: 200,
            resp['message']: 'OK',
            resp['apikey']['id']: 1,
            resp['apikey']['permission']: 'admin',
            'apikey' in resp['apikey']: True,
            'created' in resp['apikey']: True,
            'uri' in resp['apikey']: True,
        })

    @testutil.authenticate('admin')
    def test_getting_a_specific_apikey_that_does_not_exist(self):
        """Get a specific API key from an ID that doesn't exist."""
        response = self.client.get('/apikeys/0')
        resp = json.loads(response.data.decode('utf-8'))
        testutil.assertEqual(self, {
            response.status_code: 404,
            resp['status']: 404,
            resp['message']: 'API Key Not Found'
        })

    @testutil.authenticate('read')
    def test_cannot_getting_a_specific_apikey_when_read(self):
        """
        Test that you can't fetch a specific api key with read permissions.

        """
        response = self.client.get('/apikeys/1')
        resp = json.loads(response.data.decode('utf-8'))
        # Check that we get the correct response
        testutil.assertEqual(self, {
            response.status_code: 403,
            resp['status']: 403,
            resp['message']: 'Insufficient Permissions',
        })

    @testutil.authenticate('write')
    def test_cannot_getting_a_specific_apikey_when_write(self):
        """
        Test that you can't fetch a specific api key with write permissions.

        """
        response = self.client.get('/apikeys/1')
        resp = json.loads(response.data.decode('utf-8'))
        # Check that we get the correct response
        testutil.assertEqual(self, {
            response.status_code: 403,
            resp['status']: 403,
            resp['message']: 'Insufficient Permissions',
        })


if __name__ == '__main__':
    unittest.main()
