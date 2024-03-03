import requests
import pandas as pd
from datetime import datetime, timedelta


def get_reviews(days, app_id):
    """
    Fetches reviews for a given app from the Apple App Store.

    Parameters:
    days (int): The number of days from today for which reviews are to be fetched.
    App_id (str): The id of the app for which reviews are to be fetched.

    Returns:
    DataFrame: A pandas DataFrame containing the fetched reviews. The DataFrame has the following columns:
               'Username', 'Date', 'Review Text', 'Score', 'Version'
    """

    reviews_dict = {"Username": [], "Date": [], "Review Text": [], "Score": [], "Version": []}

    page_num = 1

    while True:
        url = f'https://itunes.apple.com/us/rss/customerreviews/page={page_num}/id={app_id}/sortBy=mostRecent/json'

        response = requests.get(url)

        if not response.ok:
            print("Failed to pull app reviews from Apple App Store.")
            break

        data = response.json()

        if 'feed' in data and 'entry' in data['feed']:
            for review in data['feed']['entry']:
                if review['updated']['label'].split('T')[0] >= (datetime.now() - timedelta(days=days)).strftime(
                        '%Y-%m-%d'):
                    reviews_dict['Username'].append(review['author']['name']['label'])
                    reviews_dict['Date'].append(review['updated']['label'].split('T')[0])
                    reviews_dict['Review Text'].append(review['content']['label'])
                    reviews_dict['Score'].append(review['im:rating']['label'])
                    reviews_dict['Version'].append(review['im:version']['label'])
                else:
                    break

        if page_num >= 10:
            break

        page_num += 1

    return pd.DataFrame(reviews_dict)
