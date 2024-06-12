# python -m unittest tests/unit/google_places.py
import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import pandas as pd

# Update the Python path to include the directory where the Google Places script is located
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'scraping'))

# The Google Places scraping script
from google_places import generate_grid, fetch_place_details, fetch_places, main

class TestGooglePlacesScraping(unittest.TestCase):

    def test_generate_grid(self):
        center_lat, center_lng, step, num_steps = -33.8688, 151.2093, 0.01, 2
        grid = generate_grid(center_lat, center_lng, step, num_steps)
        self.assertEqual(len(grid), (num_steps * 2 + 1) ** 2)
        self.assertIn((center_lat, center_lng), grid)

    @patch('requests.get')
    def test_fetch_place_details(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'result': {
                'name': 'Test Place',
                'formatted_address': '123 Test St, Test City',
                'place_id': 'test_place_id',
                'international_phone_number': '+1234567890',
                'website': 'http://testplace.com',
                'rating': 4.5,
                'price_level': 2,
                'types': ['test_type'],
                'geometry': {'location': {'lat': -33.8688, 'lng': 151.2093}},
                'business_status': 'OPERATIONAL',
                'opening_hours': {'weekday_text': ['Monday: 9:00 AM – 5:00 PM']},
                'photos': [{'photo_reference': 'test_photo_reference'}],
                'reviews': [{'author_name': 'Test Author', 'text': 'Test Review'}]
            }
        }
        mock_get.return_value = mock_response

        fetched_ids = set()
        details = fetch_place_details('test_api_key', 'test_place_id', fetched_ids)

        self.assertEqual(details['Name'], 'Test Place')
        self.assertEqual(details['Address'], '123 Test St, Test City')
        self.assertEqual(details['Phone Number'], '+1234567890')
        self.assertIn('Test Author: Test Review', details['Reviews'])
        self.assertIn('https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=test_photo_reference&key=test_api_key', details['Photo URLs'])

    @patch('requests.get')
    @patch('google_places.fetch_place_details')
    def test_fetch_places(self, mock_fetch_place_details, mock_get):
        mock_fetch_place_details.return_value = {
            'Name': 'Test Place',
            'Address': '123 Test St, Test City',
            'Place ID': 'test_place_id'
        }
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'results': [{'place_id': 'test_place_id'}]
        }
        mock_get.return_value = mock_response

        locations = [(-33.8688, 151.2093)]
        place_details_list = fetch_places('test_api_key', locations, 'Australia Post')

        self.assertEqual(len(place_details_list), 1)
        self.assertEqual(place_details_list[0]['Name'], 'Test Place')
        self.assertEqual(place_details_list[0]['Address'], '123 Test St, Test City')

    @patch('google_places.fetch_places')
    def test_main(self, mock_fetch_places):
        mock_fetch_places.return_value = [
            {'Name': 'Test Place', 'Address': '123 Test St, Test City', 'Place ID': 'test_place_id'}
        ]

        df = main('test_api_key', -33.8688, 151.2093, 0.01, 2)
        self.assertEqual(len(df), 1)
        self.assertIn('Name', df.columns)
        self.assertIn('Address', df.columns)

if __name__ == '__main__':
    unittest.main()
