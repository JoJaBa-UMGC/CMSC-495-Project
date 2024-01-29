import requests
from datetime import datetime
from dateutil import parser
import pandas
import pprint
from datetime import datetime, timedelta

import pytz as pytz

from app_store.app_store_reviews_reader import AppStoreReviewsReader


# def get_app_id(app_name):
#     # Pasha's key
#     # key = "AIzaSyCH-_ALlgGE0iWbDNlO7MwMZOuyKYLOU8k"
#     # Joel's key
#     # key = "AIzaSyBxO_I_8zbjO-_El9fFGlRLdLJjQ5EdHbc"
#     # Jordan's key
#     key = "AIzaSyDyC-G8JgUD_rRgJsvSIJflFqdCnTMXs9g"
#     engine = "c5a5f09a33422445a"
#
#     url = "https://www.googleapis.com/customsearch/v1?key=" + key + "&cx=" + engine + "&q=app store " + app_name
#
#     response = requests.get(url)
#     data = response.json()
#
#     return data['items'][0]['link'].split('/')[-1]


# def check_date(review_date, days):
#     d = datetime.now() - parser.parse(review_date.split('T')[0])
#
#     if d.days >= int(days):
#         return True
#
#     return False


def get_reviews(days, app_id):

    app_store_reader = AppStoreReviewsReader(app_id=app_id, country='us')

    since_time = datetime.utcnow().astimezone(pytz.utc) + timedelta(days=-days)

    reviews = app_store_reader.fetch_reviews(after=since_time)

    reviews_dict = {"Username": [],
                    "Date": [],
                    "Review Text": [],
                    "Score": [],
                    "Version": []
                    }

    for review in reviews:

        #reviews_dict['Title'].append(review.title)

        reviews_dict['Username'].append(review.author_name)

        reviews_dict['Date'].append(review.date)

        reviews_dict['Review Text'].append(review.content)

        reviews_dict['Score'].append(review.rating)

        reviews_dict['Version'].append(review.version)

    df_app = pandas.DataFrame(reviews_dict)

    return df_app

    # app_id = apple_id
    # reviews_dict = {"Username": [],
    #                 "Date": [],
    #                 "Review Text": [],
    #                 "Score": [],
    #                 "Version": []
    #                 }
    #
    # url = 'https://itunes.apple.com/us/rss/customerreviews/id=' + app_id + '/sortBy=mostRecent/json'
    # response = requests.get(url)
    #
    # if response.ok:
    #     data = response.json()
    #
    #     for review in data['feed']['entry']:
    #         if check_date(review['updated']['label'], days):
    #             reviews_dict['Username'].append(review['author']['name']['label'])
    #
    #             reviews_dict['Date'].append(review['updated']['label'].split('T')[0])
    #
    #             reviews_dict['Review Text'].append(review['content']['label'])
    #
    #             reviews_dict['Score'].append(review['im:rating']['label'])
    #
    #             reviews_dict['Version'].append(review['im:version']['label'])
    #
    #     return pandas.DataFrame(reviews_dict)
    #     # return reviews_dict
    # else:
    #     print("Failed to pull app reviews from Apple App Store.")


# def main():
#     app_search = AppFinder()
#     app_search.find_app("vain glory")
#     get_reviews(30, app_search.apple_id)
#
#
# if __name__ == '__main__':
#     main()
