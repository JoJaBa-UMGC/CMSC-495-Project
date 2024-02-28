from google_play_scraper import Sort, reviews
from datetime import datetime
from time import sleep
import pandas
import time


def check_date(review, days):
    """
       Checks if a review is older than a certain number of days.

       Parameters:
       review (dict): The review to check.
       days (int): The number of days to check against.

       Returns:
       bool: False if the review is newer than the number of days, True otherwise.
    """
    if days <= 0:
        return False
    d = datetime.now() - review['at']
    return d.days >= int(days)


def get_reviews(days, google_id):
    """
    Fetches reviews for a given app from the Google Play Store.

    Parameters:
    days (int): The number of days from today for which reviews are to be fetched.
    App_id (str): The id of the app for which reviews are to be fetched.

    Returns:
    DataFrame: A pandas DataFrame containing the fetched reviews. The DataFrame has the following columns:
               'Username', 'Date', 'Review Text', 'Score', 'Version'
    """
    reviews_dict = {"Username": [],
                    "Date": [],
                    "Review Text": [],
                    "Score": [],
                    "Version": []
                    }

    start_time = time.time()
    app_reviews = reviews_date(
        days=days,
        app_id=google_id,
        sleep_milliseconds=0,
        lang='en',
        country='nz',
        sort=Sort.NEWEST,
    )
    print("Retrieved google reviews in {} seconds".format(time.time() - start_time))
    print()

    app_reviews = [review for review in app_reviews if not check_date(review, days)]

    for review in app_reviews:
        reviews_dict['Username'].append(review['userName'])
        reviews_dict['Date'].append(review['at'])
        reviews_dict['Review Text'].append(review['content'])
        reviews_dict['Score'].append(review['score'])
        reviews_dict['Version'].append(review['reviewCreatedVersion'])

    df_app = pandas.DataFrame(reviews_dict)

    return df_app


def reviews_date(app_id: str, sleep_milliseconds: int = 0, days: int = 0, **kwargs) -> list:
    """
        Fetches reviews for a given app from the Google Play Store until a certain date.

        Parameters:
        app_id (str): The id of the app for which reviews are to be fetched.
        sleep_milliseconds (int): The number of milliseconds to sleep between fetches. Defaults to 0.
        days (int): The number of days from today until which reviews are to be fetched.
        **kwargs: Additional keyword arguments to pass to the reviews function.

        Returns:
        list: A list of reviews fetched from the Google Play Store.
    """
    kwargs.pop("count", None)
    kwargs.pop("continuation_token", None)

    continuation_token = None

    result = []

    while True:
        _result, continuation_token = reviews(
            app_id,
            count=1000,
            continuation_token=continuation_token,
            **kwargs
        )

        result += _result

        if continuation_token.token is None:
            break

        if sleep_milliseconds:
            sleep(sleep_milliseconds / 1000)

        if check_date(result[-1], days):
            break

    return result
