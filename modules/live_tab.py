from dash import dcc, html, Output, Input, State
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

def store_data(message, current_data):
    if message:
        try:
            json_data = json.loads(message)
            return json_data
        except json.JSONDecodeError as e:
            return current_data
    return current_data

def update_graph(n, data, existing_figure):
    if not data:
        raise PreventUpdate

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

def register_callbacks(app):
    app.callback(
        Output('stock-data-store', 'data'),
        [Input('event-source', 'message')],
        [State('stock-data-store', 'data')]
    )(store_data)

    app.callback(
        Output('live-stock-graph', 'figure'),
        [Input('interval-component', 'n_intervals')],
        [State('stock-data-store', 'data'), State('live-stock-graph', 'figure')]
    )(update_graph)
