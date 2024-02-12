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

    # Initialize a dictionary to store the reviews
    reviews_dict = {"Username": [], "Date": [], "Review Text": [], "Score": [], "Version": []}

    # Initialize the page number
    page_num = 1

    # Loop until break condition is met
    while True:
        # Construct the URL for the API request
        url = f'https://itunes.apple.com/us/rss/customerreviews/page={page_num}/id={app_id}/sortBy=mostRecent/json'

        # Send a GET request to the API
        response = requests.get(url)

        # If the response is not OK, print an error message and break the loop
        if not response.ok:
            print("Failed to pull app reviews from Apple App Store.")
            break

        # Parse the JSON response
        data = response.json()

        # Loop through each review in the response
        for review in data['feed']['entry']:
            # Append the username, date, review text, score, and version to the reviews dictionary
            reviews_dict['Username'].append(review['author']['name']['label'])
            reviews_dict['Date'].append(review['updated']['label'].split('T')[0])
            reviews_dict['Review Text'].append(review['content']['label'])
            reviews_dict['Score'].append(review['im:rating']['label'])
            reviews_dict['Version'].append(review['im:version']['label'])

        # If the date of the last review is older than the specified number of days,
        # or if the page number is 10 or more, break the loop
        if reviews_dict['Date'][-1] <= (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d') or page_num >= 10:
            break

        # Increment the page number
        page_num += 1

    # Return the reviews as a pandas DataFrame
    return pd.DataFrame(reviews_dict)
