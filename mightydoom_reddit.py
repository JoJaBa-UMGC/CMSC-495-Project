import praw
import pandas
import datetime

username = '_scraperbot'
password = 'vdt1BZA7ndh*tdh*rur'
client_id = '9IebaIEsSBljnLhIVdJPZw'
client_secret = 'b15GYSRUxXHYzfLnoI5aNOHedeGWTw'
user_agent = "praw_scraper_1.0"


def get_posts():
    reddit = praw.Reddit(username=username,
                         password=password,
                         client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent)

    subreddit_name = 'MightyDoom'
    subreddit = reddit.subreddit(subreddit_name)

    print(subreddit)
    print(reddit.user.me())

    posts = subreddit.top("day")

    posts_dict = {"Title": [],
                  "Date": [],
                  "Post Text": [],
                  "Score": [],
                  "Total Comments": [],
                  "Post URL": []
                  }
    for post in posts:
        # Title of each post
        posts_dict["Title"].append(post.title)

        # Text inside a post
        posts_dict["Post Text"].append(post.selftext)

        # Date post was created
        posts_dict["Date"].append(datetime.datetime.fromtimestamp(post.created_utc))

        # The score of a post
        posts_dict["Score"].append(post.score)

        # Total number of comments inside the post
        posts_dict["Total Comments"].append(post.num_comments)

        # URL of each post
        posts_dict["Post URL"].append(post.url)

    df_posts = pandas.DataFrame(posts_dict)

    print(f"# of Reddit posts: {len(df_posts)}")

    return df_posts