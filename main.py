import os
import time

import play_store_reviews
import app_store_reviews
from find_app_id import AppFinder

from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.urandom(24)


@app.route('/', methods=['POST', 'GET'])
def landing_page():
    if request.method == 'POST':
        app_name = request.form.get('app_name')
        search_period = request.form.get('search_period')
        return show_forum_report_page(app_name, search_period)

    return show_landing_page()


def show_landing_page():
    return render_template('landing.html')


@app.route('/forumreport')
def forum_report_page():
    return show_forum_report_page(1)


def show_forum_report_page(app_name, search_period):
    app_search = AppFinder()
    app_search.find_app(app_name)

    days = {
        'month': 30,
        'quarter': 91,
        'half-year': 182,
        'year': 365,
        'whole-period': -1
    }[search_period]

    df_google_reviews = play_store_reviews.get_reviews(days, app_search.google_id)

    df_appsto_reviews = app_store_reviews.get_reviews(days, app_search.apple_id)

    if len(df_google_reviews) > 0:
        google_reviews = [df_google_reviews.to_html(classes="data", header=True)]
    else:
        google_reviews = []

    if len(df_appsto_reviews) > 0:
        appstore_reviews = [df_appsto_reviews.to_html(classes="data", header=True)]
    else:
        appstore_reviews = []

    return render_template('forumreport.xhtml',
                           google_reviews=google_reviews,
                           appstore_reviews=appstore_reviews)


if __name__ == '__main__':
    app.run(debug=True)