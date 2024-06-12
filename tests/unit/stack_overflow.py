# python -m unittest tests/unit/stackoverflow.py
import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import pandas as pd
import requests

# Update the Python path to include the directory where the StackOverflow script is located
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'scraping'))

# The StackOverflow scraping script
from stackoverflow_API import fetch_questions_and_answers, strip_tags, MLStripper

class TestStackOverflowScraping(unittest.TestCase):

    @patch('requests.get')
    @patch('pandas.DataFrame.to_csv')
    def test_fetch_questions_and_answers_success(self, mock_to_csv, mock_get):
        # Mock the API responses
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'items': [
                {
                    'question_id': 1,
                    'title': 'Test Question Title',
                    'body': '<p>Test Question Body</p>',
                    'score': 10,
                    'view_count': 100,
                    'creation_date': 1609459200,
                    'last_activity_date': 1609545600
                }
            ]
        }
        mock_get.return_value = mock_response

        # Mock the fetch_answers function
        with patch('stackoverflow_API.fetch_answers', return_value=[
            {'body': '<p>Test Answer 1</p>'},
            {'body': '<p>Test Answer 2</p>'}
        ]):
            keywords = ['AusPost API']
            current_directory = os.getcwd()
            fetch_questions_and_answers(keywords, current_directory)

            # Check if the data was fetched from the correct URL
            mock_get.assert_called_with(
                'https://api.stackexchange.com/2.3/search/advanced',
                params={
                    'site': 'stackoverflow',
                    'q': 'AusPost API',
                    'sort': 'votes',
                    'order': 'desc',
                    'pagesize': 100,
                    'page': 1
                }
            )

            # Check if the DataFrame was saved to the correct file
            expected_filename = 'StackOverflowKeywords.csv'
            mock_to_csv.assert_called_once_with(os.path.join(current_directory, expected_filename), index=False)

    @patch('requests.get')
    def test_fetch_questions_and_answers_no_questions_found(self, mock_get):
        # Mock the API response with no questions
        mock_response = MagicMock()
        mock_response.json.return_value = {'items': []}
        mock_get.return_value = mock_response

        keywords = ['AusPost API']
        current_directory = os.getcwd()
        fetch_questions_and_answers(keywords, current_directory)

        # Check that the DataFrame was never created or saved
        with patch('pandas.DataFrame.to_csv') as mock_to_csv:
            self.assertFalse(mock_to_csv.called)

    def test_strip_tags(self):
        html = "<p>This is a <b>test</b>.</p>"
        expected_text = "This is a test."
        self.assertEqual(strip_tags(html), expected_text)

if __name__ == '__main__':
    unittest.main()
