import unittest
import json
import cred
import cred.test.util as testutil


class APIKeyTestCase(testutil.BaseTestCase):

    @testutil.authenticate('admin')
    def test_creating_apikey(self):
        """Test creating an API key."""
        self.assertEqual(False, True)

    @testutil.authenticate('read')
    def test_cannot_create_apikey_when_read(self):
        """Test that you can't create an api key with read permissions."""
        self.assertEqual(False, True)

    @testutil.authenticate('write')
    def test_cannot_create_apikey_when_read(self):
        """Test that you can't create an api key with write permissions."""
        self.assertEqual(False, True)

    @testutil.authenticate('admin')
    def test_getting_a_list_of_apikeys(self):
        """Get a list of API keys."""
        self.assertEqual(False, True)

    @testutil.authenticate('read')
    def test_cannot_get_a_list_of_apikeys_when_read(self):
        """Test that you can't fetch api keys with read permissions."""
        self.assertEqual(False, True)

    @testutil.authenticate('write')
    def test_cannot_get_a_list_of_apikeys_when_write(self):
        """Test that you can't fetch api keys with write permissions."""
        self.assertEqual(False, True)

    @testutil.authenticate('admin')
    def test_getting_a_specific_apikey(self):
        """Get a specific API key from ID."""
        self.assertEqual(False, True)

    @testutil.authenticate('read')
    def test_cannot_getting_a_specific_apikey_when_read(self):
        """
        Test that you can't fetch a specific api key with read permissions.

        """
        self.assertEqual(False, True)

    @testutil.authenticate('write')
    def test_cannot_getting_a_specific_apikey_when_write(self):
        """
        Test that you can't fetch a specific api key with write permissions.

        """
        self.assertEqual(False, True)


if __name__ == '__main__':
    unittest.main()
