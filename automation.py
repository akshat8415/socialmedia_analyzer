from transformers import pipeline
import os
import csv
import logging
from dotenv import load_dotenv, set_key
from instagrapi import Client
from login import login

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize the Instagram client
cl = Client()

# Initialize the BERT sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis")

def update_env_file(username, password):
    """Update credentials in the .env file."""
    env_file = '.env'
    set_key(env_file, 'INSTA_USERNAME', username)
    set_key(env_file, 'INSTA_PASSWORD', password)
    load_dotenv()  # Reload updated variables


def fetch_user_data():
    """Fetch user information."""
    try:
        user_info = cl.account_info()
        logger.info(f"User Info: {user_info}")
        return user_info
    except Exception as e:
        logger.error(f"Failed to fetch user data: {e}")


def calculate_sentiment_percentages(comments):
    """Calculate the percentage of positive and negative sentiments."""
    positive_count = 0
    negative_count = 0
    total_comments = len(comments)
    
    for c in comments:
        if c["sentiment"] == "POSITIVE":
            positive_count += 1
        elif c["sentiment"] == "NEGATIVE":
            negative_count += 1
    
    # Calculate the percentages
    positive_percentage = (positive_count / total_comments) * 100 if total_comments > 0 else 0
    negative_percentage = (negative_count / total_comments) * 100 if total_comments > 0 else 0
    
    return positive_percentage, negative_percentage


def fetch_user_posts_with_bert_sentiment():
    """
    Fetch recent posts and analyze sentiment for comments using BERT.
    Returns a list of posts with sentiment analysis results.
    """
    try:
        user_id = cl.user_id
        if not user_id:
            raise Exception("User ID not found. Ensure the client is logged in.")

        posts = cl.user_medias(user_id, 20)  # Limit to 20 posts for performance
        post_data = []

        for post in posts:
            try:
                comments = cl.media_comments(post.pk)
                sentiments = []

                for comment in comments:
                    sentiment = sentiment_analyzer(comment.text)[0]  # Use BERT to analyze sentiment
                    sentiments.append({
                        "comment": comment.text,
                        "sentiment": sentiment["label"],
                        "score": sentiment["score"]
                    })

                # Calculate positive and negative sentiment percentages for the post
                positive_percentage, negative_percentage = calculate_sentiment_percentages(sentiments)

                post_data.append({
                    "id": post.pk,
                    "caption": post.caption_text,
                    "like_count": post.like_count,
                    "comment_count": post.comment_count,
                    "timestamp": post.taken_at,
                    "positive_percentage": f"{positive_percentage:.2f}%",
                    "negative_percentage": f"{negative_percentage:.2f}%",
                    "comments": "; ".join(
                        [f'{c["comment"]} ({c["sentiment"]}, {c["score"]:.2f})' for c in sentiments]
                    )
                })

            except Exception as e:
                logger.error(f"Failed to analyze comments for post {post.pk}: {e}")

        logger.info(f"Fetched and analyzed {len(posts)} posts.")
        return post_data
    except Exception as e:
        logger.error(f"Failed to fetch user posts: {e}")


def posts_with_sentiment_to_csv(posts, file_name="user_posts_with_bert_sentiment.csv"):
    """
    Save posts and their BERT sentiment analysis to a CSV file.
    """
    try:
        # Specify the file columns
        columns = ["id", "caption", "like_count", "comment_count", "timestamp", "positive_percentage", "negative_percentage", "comments"]

        # Prepare the data
        data = []
        for post in posts:
            data.append({
                "id": post["id"],
                "caption": post["caption"],
                "like_count": post["like_count"],
                "comment_count": post["comment_count"],
                "timestamp": post["timestamp"],
                "positive_percentage": post["positive_percentage"],
                "negative_percentage": post["negative_percentage"],
                "comments": post["comments"]
            })

        # Write to CSV
        with open(file_name, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            writer.writerows(data)

        logger.info(f"Posts with BERT sentiment data saved to {file_name}")
    except Exception as e:
        logger.error(f"Failed to save posts data to CSV: {e}")


def main():
    if login(cl):  # Ensure login before proceeding
        logger.info("Login successful. Fetching data...")

        # Fetch user info
        user_info = fetch_user_data()
        if user_info:
            logger.info("User data retrieved successfully.")

        # Fetch posts with BERT sentiment analysis
        posts = fetch_user_posts_with_bert_sentiment()
        if posts:
            posts_with_sentiment_to_csv(posts)
    else:
        logger.error("Login failed. Exiting.")


if __name__ == "__main__":
    main()
