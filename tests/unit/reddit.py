# python -m unittest tests/unit/reddit.py
import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import datetime

# Update the Python path to include the directory where reddit_API.py is located
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'scraping'))

from reddit_API import fetch_and_save_reddit_posts, parse_args

class TestRedditScraping(unittest.TestCase):
    @patch('reddit_API.praw')
    @patch('reddit_API.pd.DataFrame.to_csv')
    def test_fetch_and_save_reddit_posts_success(self, mock_to_csv, mock_praw):
        # Setup mock objects
        mock_reddit = MagicMock()
        mock_praw.Reddit.return_value = mock_reddit
        mock_subreddit = MagicMock()
        mock_reddit.subreddit.return_value = mock_subreddit
        mock_submission = MagicMock(title="Test Title", url="http://testurl.com", selftext="Test Post Text", score=10)
        mock_submission.comments.list.return_value = [MagicMock(author=MagicMock(name="TestUser"), body="Test Comment", score=5)]
        mock_submission.comments.replace_more.return_value = None
        mock_subreddit.search.return_value = [mock_submission]

        # Mock the command line arguments
        test_args = [
            'script_name',
            '--client_id', 'test_client_id',
            '--client_secret', 'test_client_secret',
            '--user_agent', 'test_user_agent',
            '--search_query', 'test query',
            '--subreddit', 'all',
            '--date_from', '2021-01-01',
            '--date_to', '2021-01-02',
            '--limit', '1',
            '--save_directory', './'
        ]
        with patch.object(sys, 'argv', test_args):
            args = parse_args()

        # Call the function with mocked data
        fetch_and_save_reddit_posts(args)

        # Check if CSV was attempted to be saved
        expected_filename = 'test_query_reddit_reviews.csv'
        expected_path = os.path.join(args.save_directory, expected_filename)
        mock_to_csv.assert_called_once_with(expected_path, index=False)

        # Cleanup: Remove created file after test (if exists)
        if os.path.exists(expected_path):
            os.remove(expected_path)

    @patch('reddit_API.praw')
    def test_fetch_and_save_reddit_posts_no_posts_found(self, mock_praw):
        # Setup mock objects
        mock_reddit = MagicMock()
        mock_praw.Reddit.return_value = mock_reddit
        mock_subreddit = MagicMock()
        mock_reddit.subreddit.return_value = mock_subreddit
        mock_subreddit.search.return_value = []

        # Mock the command line arguments
        test_args = [
            'script_name',
            '--client_id', 'test_client_id',
            '--client_secret', 'test_client_secret',
            '--user_agent', 'test_user_agent',
            '--search_query', 'test query',
            '--subreddit', 'all',
            '--date_from', '2021-01-01',
            '--date_to', '2021-01-02',
            '--limit', '1',
            '--save_directory', './'
        ]
        with patch.object(sys, 'argv', test_args):
            args = parse_args()

        # Call the function with mocked data
        fetch_and_save_reddit_posts(args)

        # There should be no output file since there are no posts
        expected_filename = 'test_query_reddit_reviews.csv'
        expected_path = os.path.join(args.save_directory, expected_filename)
        self.assertFalse(os.path.exists(expected_path))

if __name__ == '__main__':
    unittest.main()
