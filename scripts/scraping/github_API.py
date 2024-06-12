import argparse
import os
import requests
import pandas as pd
import time
from datetime import datetime

def fetch_and_save_github_repos(args):
    query = ' OR '.join(args.keywords) + ' location:Australia'
    
    # Adding date filtering to the query if specified
    if args.date_from and args.date_to:
        date_from = datetime.strptime(args.date_from, '%Y-%m-%d').strftime('%Y-%m-%dT%H:%M:%SZ')
        date_to = datetime.strptime(args.date_to, '%Y-%m-%d').strftime('%Y-%m-%dT%H:%M:%SZ')
        query += f" created:{date_from}..{date_to}"

    params = {
        'q': query,
        'sort': args.sort,
        'order': args.order,
    }
    headers = {
        'Accept': 'application/vnd.github.v3+json',
    }

    try:
        response = requests.get('https://api.github.com/search/repositories', headers=headers, params=params)
        print(f"Initial response status: {response.status_code}")

        if response.status_code == 403:  # HTTP 403 for rate limit exceeded
            print("Rate limit exceeded. Waiting 60 seconds...")
            time.sleep(60)
            response = requests.get('https://api.github.com/search/repositories', headers=headers, params=params)

        response.raise_for_status()
        data = response.json()
        repos = []

        for item in data['items']:
            repos.append({
                "Repository Name": item['name'],
                "Description": item.get('description'),
                "Tags": ', '.join(item.get('topics', [])),
                "URL": item['html_url'],
                "Stars": item['stargazers_count'],
                "Forks": item['forks_count'],
                "Open Issues": item['open_issues_count'],
                "Language": item.get('language', 'Not specified'),
                "Date Published": item['created_at'],
                "Last Updated": item['updated_at'],
                "Latest Release": item.get('latest_release', 'Not specified')
            })

        if repos:
            df = pd.DataFrame(repos)
            file_name = f"{args.sort}_{args.order}_github_repos.csv"
            os.makedirs(args.save_directory, exist_ok=True)
            save_path = os.path.join(args.save_directory, file_name)
            df.to_csv(save_path, index=False)
            print(f"Exported to {save_path}")
        else:
            print("No repositories found.")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def parse_args():
    parser = argparse.ArgumentParser(description="Search GitHub repositories based on customized queries and save the results.")
    parser.add_argument("--keywords", nargs='+', default=['Australian government apps', 'Government Azure', 'COVID', 'crime', 'bushfire'], help="List of keywords to search for")
    parser.add_argument("--date_from", type=str, help="Start date for repository creation (format YYYY-MM-DD)")
    parser.add_argument("--date_to", type=str, help="End date for repository creation (format YYYY-MM-DD)")
    parser.add_argument("--sort", default='stars', choices=['stars', 'forks', 'updated'], help="Criteria for sorting the search results")
    parser.add_argument("--order", default='desc', choices=['asc', 'desc'], help="Order of sorting the search results")
    parser.add_argument("--save_directory", default="./data", help="Directory to save the output CSV file")
    return parser.parse_args()

# python github_API.py --keywords "machine learning" "artificial intelligence" --date_from 2020-01-01 --date_to 2021-01-01 --sort stars --order desc --save_directory "/path/to/save"
if __name__ == "__main__":
    args = parse_args()
    fetch_and_save_github_repos(args)
