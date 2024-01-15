from app_store.app_store_reviews_reader import AppStoreReviewsReader
import pandas
import numpy
import pycountry
import pytz
from datetime import datetime, timedelta


def get_reviews(days):
    reviews_dict = {"Username": [],
                    "Country": [],
                    "Date": [],
                    "Review Text": [],
                    "Score": [],
                    "Version": []
                    }
    since_time = datetime.utcnow().astimezone(pytz.utc) + timedelta(days=-int(days))

    errors = 0
    count = 0

    for country in pycountry.countries:
        app = AppStoreReviewsReader(app_id='1535673981', country=country.alpha_2)
        try:
            app_reviews = app.fetch_reviews(after=since_time)

            for review in app_reviews:
                print(f'appending {count}')
                count += 1
                reviews_dict['Username'].append(review.__dict__['author_name'])

                reviews_dict['Country'].append(review.__dict__['country'])

                reviews_dict['Date'].append(review.__dict__['date'])

                reviews_dict['Review Text'].append(review.__dict__['content'])

                reviews_dict['Score'].append(review.__dict__['rating'])

                reviews_dict['Version'].append(review.__dict__['version'])
        except Exception as e:
            errors += 1

    print(f"APPSTORE ERRORS: {errors}")
    print(f"# of App Store reviews: {len(reviews_dict)}")

    df_app = pandas.DataFrame(reviews_dict)

    return df_app

