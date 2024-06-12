import os
import pandas as pd
import sys

# Add the directory containing config.py to the Python path
sys.path.append(os.path.abspath(os.path.join('..', '..')))

from config import REDDIT_RAW_DATA_DIR, MERGED_DATA_DIR

# Define the directory containing the datasets
DATA_DIR = REDDIT_RAW_DATA_DIR
OUTPUT_DIR = MERGED_DATA_DIR
OUTPUT_FILE = "merged_reddit_reviews.csv"
LOG_FILE = "merge_errors.log"

def extract_service_name(filename):
    """Extract the service name from the filename."""
    if filename.endswith("_reddit_reviews.csv"):
        return filename.replace("_reddit_reviews.csv", "").replace("_", " ")
    return "Unknown"

def merge_reddit_data(data_dir, output_dir, output_file, log_file):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Clear or create the log file
    with open(log_file, 'w') as f:
        f.write("")

    # List to hold dataframes
    df_list = []
    
    # Define a dictionary to specify data types for certain columns
    dtype_dict = {
        'Title': str,
        'URL': str,
        'Post Text': str,
        'Upvotes': 'Int64',
        'Comment Author': str,
        'Comment': str,
        'Comment Upvotes': 'Int64',
        'Submission Date': str,
        'Comment Date': str
    }
    
    # Iterate over all CSV files in the directory
    for filename in os.listdir(data_dir):
        if filename.endswith(".csv"):
            file_path = os.path.join(data_dir, filename)
            service_name = extract_service_name(filename)
            print(f"Processing file: {file_path}")
            try:
                # Read the CSV file with specified data types
                df = pd.read_csv(file_path, dtype=dtype_dict, low_memory=False)
                
                # Convert date columns to datetime, coercing errors to NaT
                df['Submission Date'] = pd.to_datetime(df['Submission Date'], errors='coerce')
                df['Comment Date'] = pd.to_datetime(df['Comment Date'], errors='coerce')
                
                # Add the service name column
                df['Service Name'] = service_name
                
                df_list.append(df)
            except pd.errors.DtypeWarning as e:
                with open(log_file, 'a') as f:
                    f.write(f"Warning while processing {file_path}: {e}\n")
            except Exception as e:
                with open(log_file, 'a') as f:
                    f.write(f"Error while processing {file_path}: {e}\n")
    
    # Concatenate all dataframes
    merged_df = pd.concat(df_list, ignore_index=True)
    
    # Define the output file path
    output_file_path = os.path.join(output_dir, output_file)
    
    # Save the merged dataframe to a CSV file
    merged_df.to_csv(output_file_path, index=False)
    print(f"Merged data saved to {output_file_path}")

if __name__ == "__main__":
    merge_reddit_data(DATA_DIR, OUTPUT_DIR, OUTPUT_FILE, LOG_FILE)
