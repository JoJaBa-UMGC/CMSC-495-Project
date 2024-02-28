import os
import requests
from dotenv import load_dotenv

load_dotenv()


class AppFinder:
    """
    A class used to find the Google Play and Apple App Store IDs of a given app.

    Attributes
    ----------
    google_id : str
        the Google Play ID of the app
    apple_id : str
        the Apple App Store ID of the app
    google_search_api_key : str
        the API key for Google's Custom Search JSON API
    engine : str
        the search engine ID for Google's Custom Search JSON API

    Methods
    -------
    find_app(app_name)
        Finds the Google Play and Apple App Store IDs of the given app.
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the AppFinder object.

        Parameters
        ----------
        None
        """

        self.google_id = ""
        self.apple_id = ""
        self.google_search_api_key = os.getenv('GOOGLE_SEARCH_API_KEY')
        self.engine = "c5a5f09a33422445a"

    def find_app(self, app_name):
        """
        Finds the Google Play and Apple App Store IDs of the given app.

        Parameters
        ----------
        app_name : str
            the name of the app

        Returns
        -------
        None
        """

        url = (f"https://www.googleapis.com/customsearch/v1?key={self.google_search_api_key}&cx={self.engine}&q=app "
               f"store {app_name}")

        data = requests.get(url).json()
        if 'items' not in data:
            return

        for item in data['items']:
            if "apps.apple.com" in item['displayLink']:
                self.apple_id = item['link'].split('/')[-1].split('id')[1]

            if "play.google.com" in item['displayLink']:
                self.google_id = item['link'].split('/')[-1].split('id=')[1].split('&hl=')[0]

            if self.google_id and self.apple_id:
                break

    def no_id(self):
        """
            Checks if the Google Play and Apple App Store IDs are empty.

            Returns:
            bool: True if either ID is empty, False otherwise.
        """
        if self.apple_id.__len__() == 0 or self.google_id.__len__() == 0:
            return True
        return False
