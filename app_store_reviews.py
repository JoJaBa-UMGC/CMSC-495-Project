import time

import requests
import pandas
from datetime import datetime, timedelta


def get_page(app_id, page_num, reviews_dict):

    url = 'https://itunes.apple.com/us/rss/customerreviews/page=' + str(page_num) + '/id=' + app_id + '/sortBy=mostRecent/json'
    response = requests.get(url)

    if response.ok:

        data = response.json()

        for review in data['feed']['entry']:
            # if check_date(review['updated']['label'], days):
            reviews_dict['Username'].append(review['author']['name']['label'])

            reviews_dict['Date'].append(review['updated']['label'].split('T')[0])

            reviews_dict['Review Text'].append(review['content']['label'])

            reviews_dict['Score'].append(review['im:rating']['label'])

            reviews_dict['Version'].append(review['im:version']['label'])
    else:
        print("Failed to pull app reviews from Apple App Store.")


def get_reviews(days, app_id):

    start_time = time.time()

    page_num = 1

    reviews_dict = {"Username": [],
                    "Date": [],
                    "Review Text": [],
                    "Score": [],
                    "Version": []
                    }

    get_page(app_id, page_num, reviews_dict)

    while reviews_dict['Date'][-1] > (datetime.now() - timedelta(days=days)).strftime(
            '%Y-%m-%d') and page_num < 11:
        page_num += 1
        get_page(app_id, page_num, reviews_dict)

    print("Retrieved apple reviews in {} seconds".format(time.time() - start_time))

    return pandas.DataFrame(reviews_dict)

    df_app = pandas.DataFrame(reviews_dict)

    return df_app
