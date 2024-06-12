import os
import argparse
import pandas as pd
import praw
import datetime
from prawcore.exceptions import RequestException, ResponseException, TooManyRequests
from datetime import datetime as dt

def fetch_and_save_reddit_posts(args):
    reddit = praw.Reddit(
        client_id=args.client_id,
        client_secret=args.client_secret,
        user_agent=args.user_agent,
    )

    subreddit = reddit.subreddit(args.subreddit)

    posts = []
    try:
        for submission in subreddit.search(args.search_query, 
                                           limit=args.limit, 
                                           syntax='cloudsearch', 
                                           time_filter='custom', 
                                           after=args.date_from.timestamp(), 
                                           before=args.date_to.timestamp()):
            submission_date = dt.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S')
            try:
                submission.comments.replace_more(limit=None)
                for comment in submission.comments.list():
                    comment_date = dt.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')
                    posts.append({
                        "Title": submission.title,
                        "URL": submission.url,
                        "Post Text": submission.selftext,
                        "Upvotes": submission.score,
                        "Comment Author": comment.author.name if comment.author else "Deleted",
                        "Comment": comment.body,
                        "Comment Upvotes": comment.score,
                        "Submission Date": submission_date,
                        "Comment Date": comment_date
                    })
            except TooManyRequests:
                print("Rate limit exceeded. Waiting 60 seconds...")
                time.sleep(60)  # Wait for 60 seconds before continuing
    except (RequestException, ResponseException) as e:
        print(f"An error occurred: {e}")

    if posts:
        df = pd.DataFrame(posts)
        file_name = f"{args.search_query.replace(' ', '_')}_reddit_reviews.csv"
        save_path = os.path.join(args.save_directory, file_name)
        df.to_csv(save_path, index=False)
        print(f"Exported to {save_path}")
    else:
        print("No posts found.")

def parse_args():
    parser = argparse.ArgumentParser(description="Scrape Reddit posts based on search queries and time filters.")
    parser.add_argument("--client_id", required=True, help="Client ID for Reddit API")
    parser.add_argument("--client_secret", required=True, help="Client Secret for Reddit API")
    parser.add_argument("--user_agent", required=True, help="User Agent for Reddit API")
    parser.add_argument("--search_query", required=True, help="Search query for Reddit posts")
    parser.add_argument("--subreddit", default="all", help="Subreddit to search, defaults to 'all'")
    parser.add_argument("--date_from", type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'), required=True, help="Start date YYYY-MM-DD")
    parser.add_argument("--date_to", type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'), required=True, help="End date YYYY-MM-DD")
    parser.add_argument("--limit", type=int, default=100, help="Limit on the number of posts to fetch")
    parser.add_argument("--save_directory", default="./", help="Directory to save the output CSV file")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    fetch_and_save_reddit_posts(args)
