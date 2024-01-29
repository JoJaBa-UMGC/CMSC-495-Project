from google_play_scraper import Sort, reviews_all
from datetime import datetime
import pandas
import numpy
import pycountry
import time


def check_date(review, days):
    d = datetime.now() - review['at']
    if d.days >= int(days):
        return True

    return False


def get_reviews(days, google_id):
    reviews_dict = {"Username": [],
                    "Date": [],
                    "Review Text": [],
                    "Score": [],
                    "Version": [],
                    "Replied": []
                    }

    app_reviews = reviews_all(
        days=days,
        app_id=google_id,
        sleep_milliseconds=0,  # defaults to 0
        lang='en',  # defaults to 'en'
        country='nz',  # defaults to 'us'
        sort=Sort.NEWEST,  # defaults to Sort.MOST_RELEVANT
    )

    app_reviews = [review for review in app_reviews if not check_date(review, days)]

    for review in app_reviews:

        reviews_dict['Username'].append(review['userName'])

        reviews_dict['Date'].append(review['at'])

        reviews_dict['Review Text'].append(review['content'])

        reviews_dict['Score'].append(review['score'])

        reviews_dict['Version'].append(review['reviewCreatedVersion'])

        reviews_dict['Replied'].append(review['replyContent'])

    # print(f"# of Google Play reviews: {len(reviews_dict)}")

    df_app = pandas.DataFrame(reviews_dict)

    return df_app
