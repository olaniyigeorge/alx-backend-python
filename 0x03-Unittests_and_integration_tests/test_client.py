#!/usr/bin/env python3

"""
Unit tests for GithubOrgClient class in client.py.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Test cases for the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct data.

        Ensures get_json is called once with the expected URL and
        that no real HTTP requests are made.
        """
        expected_data = {
            "name": f"{org_name.capitalize()} Org",
            "repos_url": f"https://api.github.com/orgs/{org_name}/repos"
        }

        mock_get_json.return_value = expected_data

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, expected_data)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """
        Test that _public_repos_url returns the correct value
        based on the mocked org payload.
        """
        expected_url = "https://api.github.com/orgs/test_org/repos"
        mock_org_payload = {
            "repos_url": expected_url
        }

        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = mock_org_payload

            client = GithubOrgClient("test_org")
            result = client._public_repos_url

            self.assertEqual(result, expected_url)



if __name__ == "__main__":
    unittest.main()
