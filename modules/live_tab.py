from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import json
from dash_extensions import EventSource
from dash.exceptions import PreventUpdate

def get_layout():
    layout = html.Div([
        dcc.Graph(id='live-stock-graph'),
        dcc.Store(id='stock-data-store'),
        EventSource(id='event-source', url='http://localhost:5000/stocks_data'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000,
            n_intervals=0
        )
    ])
    return layout

def register_callbacks(app):
    """
    Registers callbacks necessary for the live tab.
    """

    @app.callback(
        Output('stock-data-store', 'data'),
        [Input('event-source', 'message')],
        [State('stock-data-store', 'data')]
    )
    def store_data(message, current_data):
        if message:
            try:
                # Directly parse the message as JSON
                json_data = json.loads(message)
                return json_data
            except json.JSONDecodeError as e:
                # Return current data without updating
                return current_data
        # If message is None, return the current data without updating
        return current_data

    # Callback to update the graph using data from Store component
    @app.callback(
        Output('live-stock-graph', 'figure'),
        [Input('interval-component', 'n_intervals')],
        [State('stock-data-store', 'data'),
        State('live-stock-graph', 'figure')]
    )
    def update_graph(n, json_data, existing_figure):
        if not json_data:
            raise PreventUpdate

        # Use json_data directly as it's already a dictionary
        data = json_data

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
