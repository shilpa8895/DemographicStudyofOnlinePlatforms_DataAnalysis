# python -m unittest tests/unit/github.py

import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Update the Python path to include the directory where github_API.py is located
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'scraping'))

from github_API import fetch_and_save_github_repos, parse_args

class TestGitHubAPI(unittest.TestCase):
    @patch('github_API.requests.get')
    def test_fetch_and_save_github_repos(self, mock_get):
        # Setup mock for HTTP response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'items': [
                {
                    'name': 'test_repo',
                    'description': 'A test repository',
                    'html_url': 'http://github.com/test_repo',
                    'stargazers_count': 100,
                    'forks_count': 50,
                    'open_issues_count': 10,
                    'language': 'Python',
                    'created_at': '2020-01-01T00:00:00Z',
                    'updated_at': '2020-01-02T00:00:00Z',
                    'topics': [],
                    'latest_release': '1.0.0'
                }
            ]
        }
        mock_get.return_value = mock_response

        # Mock the command line arguments
        test_args = [
            'script_name',
            '--keywords', 'test', 'repo',
            '--date_from', '2020-01-01',
            '--date_to', '2020-12-31',
            '--sort', 'stars',
            '--order', 'desc',
            '--save_directory', '../data/tests'
        ]
        with patch.object(sys, 'argv', test_args):
            args = parse_args()

        # Run the function under test
        fetch_and_save_github_repos(args)

        # Assert the file was created in the specified directory
        expected_path = os.path.join(args.save_directory, 'stars_desc_github_repos.csv')
        self.assertTrue(os.path.exists(expected_path))

        # Clean up if necessary (remove created files, etc.)
        os.remove(expected_path)

if __name__ == '__main__':
    unittest.main()
