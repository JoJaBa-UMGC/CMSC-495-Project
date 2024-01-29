import requests
from datetime import datetime
from dateutil import parser
import pandas


class AppFinder:
    google_id = ""
    apple_id = ""

    def find_app(self, app_name):
        # Pasha's key
        # key = "AIzaSyCH-_ALlgGE0iWbDNlO7MwMZOuyKYLOU8k"
        # Joel's key
        # key = "AIzaSyBxO_I_8zbjO-_El9fFGlRLdLJjQ5EdHbc"
        # Jordan's key
        key = "AIzaSyDyC-G8JgUD_rRgJsvSIJflFqdCnTMXs9g"
        engine = "c5a5f09a33422445a"

        url = "https://www.googleapis.com/customsearch/v1?key=" + key + "&cx=" + engine + "&q=app store " + app_name

        response = requests.get(url)
        data = response.json()

        for item in data['items']:
            if item['displayLink'] == "apps.apple.com":
                self.set_apple_id(item['link'])
            if item['displayLink'] == "play.google.com":
                self.set_google_id(item['link'])

            if self.google_id != "" and self.apple_id != "":
                break

    def set_apple_id(self, link):
        self.apple_id = link.split('/')[-1].split('id')[1]

    def set_google_id(self, link):
        self.google_id = link.split('/')[-1].split('id=')[1].split('&hl=')[0]
