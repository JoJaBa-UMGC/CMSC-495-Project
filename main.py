import os

from flask import Flask, render_template, request, session

import app_store_reviews
import filtering
import play_store_reviews
import graph_generator
import csv_generator
from find_app_id import AppFinder

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'

search_periods = {'month': 30, 'two-months': 60, 'quarter': 91}


def get_reviews_for_platform(days, platform):
    """Fetch reviews for a given platform and return HTML or an empty list."""
    if platform == 'Google':
        df_reviews = play_store_reviews.get_reviews(days, session.get('google_id'))
    else:
        df_reviews = app_store_reviews.get_reviews(days, session.get('apple_id'))

    graph = graph_generator.generate_graph(df_reviews, platform + " Reviews Scores")

    df_reviews = filtering.sort_reviews(df_reviews, session.get('sorting_option'))

    return df_reviews, graph


def reviews_to_html(reviews):
    if reviews is not None and len(reviews) > 0:
        reviews.index = range(1, len(reviews) + 1)
        return [reviews.to_html(classes="data", header=True)]


@app.route('/', methods=['POST', 'GET'])
def landing_page():
    if request.method == 'POST':
        app_name = request.form.get('app_name')
        search_period = request.form.get('search_period', 'month')
        sorting_option = request.form.get('sorting_option', 'score')
        return show_forum_report_page(app_name, search_period, sorting_option)
    return render_template('landing.html')


def show_forum_report_page(app_name, search_period, sorting_option):
    global google_reviews, appstore_reviews
    days = search_periods.get(search_period, 30)

    app_search = AppFinder()
    app_search.find_app(app_name)

    session['google_id'] = app_search.google_id
    session['apple_id'] = app_search.apple_id
    session['sorting_option'] = sorting_option

    google_reviews = get_reviews_for_platform(days, 'Google')
    appstore_reviews = get_reviews_for_platform(days, 'Apple')

    return render_template('review_display.html',
                           google_reviews=reviews_to_html(google_reviews[0]),
                           appstore_reviews=reviews_to_html(appstore_reviews[0]),
                           google_graph_json=google_reviews[1],
                           apple_graph_json=appstore_reviews[1])


@app.route('/google')
def google_csv():
    return csv_generator.generate_csv(google_reviews[0], "Google")


@app.route('/apple')
def apple_csv():
    return csv_generator.generate_csv(appstore_reviews[0], "Apple")


if __name__ == '__main__':
    app.run(debug=True)
