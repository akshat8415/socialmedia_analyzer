# import time
# import schedule
# import keyring
# import random
# import os



# Example usage of update_env_file function
# Uncomment the lines below to update the .env file with new credentials
# new_username = input("Enter your new Instagram username: ")
# new_password = input("Enter your new Instagram password: ")
# update_env_file(new_username, new_password)



# Function to like and comment on recent posts of a hashtag
# def like_and_comment_on_hashtag_posts(hashtag, amount=3):
#     try:
#         medias = cl.hashtag_medias_recent(hashtag, amount=amount)
#         for i, media in enumerate(medias):
#             cl.media_like(media.id)
#             cl.media_comment(media.id, "super cool")
#             print(f'Liked and commented on post number {i + 1} of hashtag: {hashtag}')
#     except Exception as e:
#         print(f"Error while liking/commenting on posts: {e}")

# Function to follow users by hashtag
# def follow_users_by_hashtag(hashtag): 
#     try:
#         users = cl.hashtag_users(hashtag)
#         for user in users:
#             cl.follow(user.pk)
#             print(f"Followed user: {user.username}")
#     except Exception as e:
#         print(f"Error while following users: {e}")

# Function to schedule a post
# def schedule_post(image_path, caption, post_time):
#     schedule.every().day.at(post_time).do(post_image, image_path, caption)
#     print(f"Scheduled post for {post_time}: {caption}")

# # Function to post an image
# def post_image(image_path, caption):
#     try:
#         cl.photo_upload(image_path, caption)
#         print(f"Posted: {caption}")
#     except Exception as e:
#         print(f"Failed to post image: {e}")

# Function to run scheduled tasks
# def run_schedule():
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# def like_recent_posts_from_followed_users(amount=3):
#     try:
#         followed_usernames =cl.user_following_gql(cl.user_id)  # This returns a list of usernames
        
#         for username in followed_usernames:
#             try:
#                 user = cl.user_info_by_username(username)  # Fetch user info by username
#                 if user:  # Check if user info was retrieved successfully
#                     medias = cl.user_medias(user.pk, amount)  # Now access the pk attribute
#                     for media in medias:
#                         cl.media_like(media.id)  # Like the media
#                         print(f'Liked post from user: {user.username}')
#                         time.sleep(1)  # Sleep to avoid rate limiting
#                         break  # Exit after liking one post from this user
#                 else:
#                     print(f"User  not found: {username}")
#             except Exception as e:
#                 print(f"Error retrieving user info for {username}: {e}")
#                 time.sleep(1)  # Sleep to avoid rate limiting
#     except Exception as e:
#         print(f"Error while liking posts from followed users: {e}")

#     # like_recent_posts_from_followed_users(amount=3) #function call 
#     hashtags = ["sunset", "nature", "travel", "photography", "landscape"]  # List of hashtags
#     random_hashtag = random.choice(hashtags)
#     # # Like and comment on recent posts for a specific hashtag
#     like_and_comment_on_hashtag_posts(random_hashtag, amount=3)

    # Follow users by hashtag
    # follow_users_by_hashtag([random_hashtag])

    # # Example of scheduling a post (modify the path and caption accordingly)
    # schedule_post('path___t0__image.jpg', ' caption here with #sunset', '09:00')

    # # Start the scheduling loop
    # run_schedule()