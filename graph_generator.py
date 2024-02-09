
import json
import plotly.utils as putil
import plotly.express as px


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
