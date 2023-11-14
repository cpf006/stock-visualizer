# Import necessary libraries
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import json
from dash_extensions import EventSource

def get_layout():
    layout = html.Div([
        html.H3('Real-Time Stock Data'),
        dcc.Graph(id='live-stock-graph'),
        # Update the URL to point to your quotes publisher server
        EventSource(id='event-source', url='http://localhost:5000/stocks_data')
    ])
    return layout

def register_callbacks(app):
    """
    Registers callbacks necessary for the live tab.
    """

    @app.callback(
        Output('live-stock-graph', 'figure'),
        [Input('event-source', 'data')],
        [State('live-stock-graph', 'figure')]
    )
    def update_graph(json_data, existing_figure):
        if json_data is None:
            # No data yet, don't update
            raise dash.exceptions.PreventUpdate
        
        # Parse the incoming JSON data
        data = json.loads(json_data)

        # Create a new figure if it doesn't exist yet
        if existing_figure is None or not existing_figure:
            figure = {
                'data': [],
                'layout': go.Layout(
                    title='Live Stock Prices',
                    xaxis={'title': 'Time'},
                    yaxis={'title': 'Price'},
                    showlegend=True
                )
            }
        else:
            figure = existing_figure

        # Update the graph with new data
        new_traces = []
        timestamps = data.pop('TIMESTAMP', None)
        if timestamps:
            for stock, prices in data.items():
                new_traces.append(go.Scatter(
                    x=timestamps,
                    y=prices,
                    mode='lines+markers',
                    name=stock
                ))
        
        figure['data'] = new_traces

        return figure