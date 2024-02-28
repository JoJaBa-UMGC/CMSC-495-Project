import os

import pandas

import login

from flask import Flask, render_template, request, session

import app_store_reviews
import play_store_reviews
import graph_generator
import csv_generator
from find_app_id import AppFinder

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'

search_periods = {'month': 30, 'two-months': 60, 'quarter': 91}

runningLocal = False

sentimentWords = {
    'positive': ["amazing", "awesome", "brilliant", "fantastic", "excellent", "fabulous", "wonderful", "perfect", "incredible",
                 "exceptional", "positive", "delightful", "pleasing", "enjoyable", "spectacular", "magnificent", "marvelous",
                 "outstanding", "superb", "great", "happy", "joyful", "lovely", "charming", "cheerful", "satisfying", "gratifying",
                 "beautiful", "elegant", "exquisite", "gorgeous", "fine", "radiant", "splendid", "stunning", "admirable", "glorious",
                 "pretty", "nice", "pleasant", "agreeable", "breathtaking", "heartwarming", "inspiring", "uplifting", "thrilling",
                 "successful", "victorious", "profitable", "beneficial"],
    'negative': ["awful", "terrible", "horrible", "dreadful", "poor", "bad", "worse", "worst", "unpleasant", "disappointing",
                 "unsatisfactory", "lamentable", "deplorable", "atrocious", "appalling", "dismal", "depressing", "dire", "gloomy",
                 "sad", "unhappy", "miserable", "sorrowful", "melancholy", "grief-stricken", "heartbroken", "anguished", "distressing",
                 "painful", "tragic", "harmful", "damaging", "destructive", "injurious", "pernicious", "fatal", "deadly", "lethal",
                 "noxious", "detrimental", "negative", "disadvantageous", "unfavorable", "adverse", "hateful", "hostile", "resentful",
                 "bitter", "angry", "irate", "outraged"]
}


def sort_reviews(reviews, by):
    """
    Function to sort reviews based on different criteria.

    Parameters:
    reviews (DataFrame): The reviews dataframe.
    by (str): The criteria to sort by. Can be 'Score', 'Review Text', 'No Text', 'Sentiment', or any other column name.

    Returns:
    DataFrame: The sorted reviews dataframe.
    """
    # Sort by score
    if by == 'score':
        return reviews.sort_values(by='Score', ascending=False)
    # Sort by review text
    elif by == 'text':
        return reviews[reviews['Review Text'].notnull()].sort_values(by='Date', ascending=False)
    # Sort by no text
    elif by == 'no-text':
        return reviews[reviews['Review Text'].isnull()].sort_values(by='Date', ascending=False)
    # Sort by sentiment
    elif by == 'positive' or by == 'negative' or by == 'neutral':
        # Convert score to numeric
        reviews['Score'] = pandas.to_numeric(reviews['Score'], errors='coerce')
        # Filter by positive sentiment
        if by == 'positive':
            filtered_reviews = reviews[
                (reviews['Review Text'].str.contains('|'.join(sentimentWords[by]), na=False)) &
                (reviews['Score'] >= 4)
                ]
        # Filter by negative sentiment
        elif by == 'negative':
            filtered_reviews = reviews[
                (reviews['Review Text'].str.contains('|'.join(sentimentWords[by]), na=False)) &
                (reviews['Score'] <= 2)
                ]
        # Filter by neutral sentiment
        else:
            filtered_reviews = reviews[reviews['Score'] == 3]
        return filtered_reviews.sort_values(by='Date', ascending=False)
    # Default sort by date
    else:
        return reviews.sort_values(by='Date', ascending=False)


def get_app(config_filename):
    """
        Load the app configuration from a file.

        Parameters:
        config_filename (str): The name of the configuration file.

        Returns:
        Flask: The configured Flask app.
    """
    app.config.from_pyfile(config_filename)
    return app


def get_reviews_for_platform(days, platform):
    """
    Fetch reviews for a given platform and return HTML or an empty list.

    Parameters:
    days (int): The number of days to fetch reviews for.
    platform (str): The platform to fetch reviews from. Can be 'Google' or 'Apple'.

    Returns:
    DataFrame, str: The reviews dataframe and the graph as a JSON string.
    """
    if platform == 'Google':
        df_reviews = play_store_reviews.get_reviews(days, session.get('google_id'))
    else:
        df_reviews = app_store_reviews.get_reviews(days, session.get('apple_id'))

    graph = graph_generator.generate_graph(df_reviews, platform + " Reviews Scores")

    df_reviews = sort_reviews(df_reviews, session.get('sorting_option'))

    return df_reviews, graph


def reviews_to_html(reviews):
    """
        Convert a reviews dataframe to HTML.

        Parameters:
        reviews (DataFrame): The reviews dataframe.

        Returns:
        list: A list containing the HTML representation of the reviews dataframe.
    """
    if reviews is not None and len(reviews) > 0:
        reviews.index = range(1, len(reviews) + 1)
        return [reviews.to_html(classes="data", header=True)]


@app.route('/', methods=['POST', 'GET'])
def landing_page():
    """
        The landing page route. Handles both GET and POST requests.

        Returns:
        str: The HTML to render.
    """
    if not login.session.get('logged_in'):
        if not runningLocal:
            return login.login()
    if request.method == 'POST':
        app_name = request.form.get('app_name')
        search_period = request.form.get('search_period', 'month')
        sorting_option = request.form.get('sorting_option', 'score')
        return show_forum_report_page(app_name, search_period, sorting_option)
    if 'logged_in' not in session or not session['logged_in']:
        if not runningLocal:
            return login.login()
    return render_template('landing.html')


def show_forum_report_page(app_name, search_period, sorting_option):
    """
        Show the forum report page.

        Parameters:
        app_name (str): The name of the app to fetch reviews for.
        search_period (str): The search period to fetch reviews for.
        sorting_option (str): The option to sort the reviews by.

        Returns:
        str: The HTML to render.
    """
    global google_reviews, appstore_reviews
    days = search_periods.get(search_period, 30)

    app_search = AppFinder()
    app_search.find_app(app_name)
    if app_search.no_id():
        return render_template('landing.html', error=f"No app by the name {app_name} was found.")
    session['google_id'] = app_search.google_id
    session['apple_id'] = app_search.apple_id
    session['sorting_option'] = sorting_option

    google_reviews = get_reviews_for_platform(days, 'Google')
    appstore_reviews = get_reviews_for_platform(days, 'Apple')

    return render_template('search_results.html',
                           google_reviews=reviews_to_html(google_reviews[0]),
                           appstore_reviews=reviews_to_html(appstore_reviews[0]),
                           google_graph_json=google_reviews[1],
                           apple_graph_json=appstore_reviews[1])


@app.route('/google')
def google_csv():
    """
        Generate a CSV file for Google reviews.

        Returns:
        str: The CSV file as a string.
    """
    return csv_generator.generate_csv(google_reviews[0], "Google")


@app.route('/apple')
def apple_csv():
    """
        Generate a CSV file for Apple reviews.

        Returns:
        str: The CSV file as a string.
    """
    return csv_generator.generate_csv(appstore_reviews[0], "Apple")


@app.route('/logout')
def logout():
    """
        Log out the user.

        Returns:
        str: The HTML to render.
    """
    print('logging out')
    return login.logout()


if __name__ == '__main__':
    runningLocal = True
    app.run(debug=True)