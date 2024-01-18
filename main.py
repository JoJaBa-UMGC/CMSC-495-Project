import os

import pandas

import mightydoom_googleplay
import mightydoom_appstore

from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = os.urandom(24)

# Testing -Jordan Kozlowski

@app.route('/', methods=['POST', 'GET'])
def landing_page():
    if request.method == 'POST':
        days = request.form.get('days')
        return show_forum_report_page(days)

    return show_landing_page()


def show_landing_page():
    return render_template('landing.xhtml')


@app.route('/forumreport')
def forum_report_page():
    return show_forum_report_page(1)


def show_forum_report_page(days):
    df_google_reviews = mightydoom_googleplay.get_reviews(days)

    if len(df_google_reviews) > 0:
        google_reviews = [df_google_reviews.to_html(classes="data", header=True)]
    else:
        google_reviews = []

    df_appstore_reviews = mightydoom_appstore.get_reviews(days)

    if len(df_appstore_reviews) > 0:
        appstore_reviews = [df_appstore_reviews.to_html(classes="data", header=True)]
    else:
        appstore_reviews = []

    return render_template('forumreport.xhtml',
                           google_reviews=google_reviews,
                           appstore_reviews=appstore_reviews)


if __name__ == '__main__':
    app.run()
