import base64
import io

from flask import Flask, render_template
import pandas as pd
import json
import plotly.utils as putil
import plotly.express as px

import app_store_reviews
import find_app_id
import play_store_reviews

APP_NAME = 'mighty doom'
DAYS = 30

app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/', methods=['GET'])
def graph_test():
    app_ids = find_app_id.AppFinder()
    app_ids.find_app(APP_NAME)
    google_df = play_store_reviews.get_reviews(DAYS, app_ids.google_id)
    apple_df = app_store_reviews.get_reviews(DAYS, app_ids.apple_id)
    google_graph_json = generate_graph(google_df, 'Google Review Scores')
    apple_graph_json = generate_graph(apple_df, 'Apple Review Scores')
    return render_template('graph.html',
                           google_graph_json=google_graph_json, apple_graph_json=apple_graph_json)


def generate_graph(reviews_dataframe, graph_title):
    scores_dataframe = (reviews_dataframe['Score']
                        .value_counts()
                        .reset_index(name='counts')
                        .rename(columns={'index': 'Review Score', 'counts': 'Score Total'})
                        .sort_values(by=['Review Score'], ascending=False))
    print(scores_dataframe)
    graph = px.bar(scores_dataframe, x='Review Score', y='Score Total', barmode='group', title=graph_title)
    graph_json = json.dumps(graph, cls=putil.PlotlyJSONEncoder)
    return graph_json


if __name__ == '__main__':
    app.run(debug=True)
