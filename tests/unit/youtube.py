# python -m unittest tests/unit/youtube.py
import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import pandas as pd

# Update the Python path to include the directory where the YouTube script is located
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'scraping'))

# The YouTube merging script
def merge_youtube_data():
    dataframes = []
    for filename in os.listdir('.'):
        if filename.endswith('.csv'):
            df = pd.read_csv(filename)
            service_name = os.path.splitext(filename)[0]
            df['serviceName'] = service_name
            dataframes.append(df)
    merged_df = pd.concat(dataframes, ignore_index=True)
    merged_df.to_csv('merged_youtubeData.csv', index=False)
    print('Files merged successfully!')

class TestYouTubeMerging(unittest.TestCase):

    @patch('os.listdir')
    @patch('pandas.read_csv')
    @patch('pandas.DataFrame.to_csv')
    def test_merge_youtube_data_success(self, mock_to_csv, mock_read_csv, mock_listdir):
        # Mock the files in the directory
        mock_listdir.return_value = ['service1.csv', 'service2.csv']

        # Mock the DataFrames
        df1 = pd.DataFrame({'data': [1, 2, 3]})
        df2 = pd.DataFrame({'data': [4, 5, 6]})
        mock_read_csv.side_effect = [df1, df2]

        # Call the function
        merge_youtube_data()

        # Check if the data was read from the correct files
        mock_read_csv.assert_any_call('service1.csv')
        mock_read_csv.assert_any_call('service2.csv')

        # Check if the DataFrame was saved to the correct file
        expected_filename = 'merged_youtubeData.csv'
        mock_to_csv.assert_called_once_with(expected_filename, index=False)

    @patch('os.listdir')
    @patch('pandas.read_csv')
    @patch('pandas.DataFrame.to_csv')
    def test_merge_youtube_data_no_csv_files(self, mock_to_csv, mock_read_csv, mock_listdir):
        # Mock no CSV files in the directory
        mock_listdir.return_value = []

        # Call the function
        merge_youtube_data()

        # Check that read_csv was never called
        mock_read_csv.assert_not_called()

        # Check that to_csv was never called
        mock_to_csv.assert_not_called()

if __name__ == '__main__':
    unittest.main()
