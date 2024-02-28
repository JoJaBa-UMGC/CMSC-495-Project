import json
import plotly.express as px
import plotly.utils as putil


def generate_graph(reviews_dataframe, graph_title):
    """
    Generates a bar graph of review scores from a DataFrame.

    Parameters:
    - reviews_dataframe: A pandas DataFrame containing a 'Score' column, or None.
    - graph_title: A string specifying the title of the graph.

    Returns:
    - A JSON string representing the generated graph, or an empty JSON object if the input is None or empty.
    """

    if reviews_dataframe.empty:
        return json.dumps({})

    scores_dataframe = (reviews_dataframe['Score']
                        .value_counts()
                        .reset_index(name='counts')
                        .rename(columns={'index': 'Review Score', 'counts': 'Score Total'})
                        .sort_values(by=['Review Score'], ascending=True))

    graph = px.bar(scores_dataframe, x='Review Score', y='Score Total', barmode='group', title=graph_title)

    graph_json = json.dumps(graph, cls=putil.PlotlyJSONEncoder)

    return graph_json
