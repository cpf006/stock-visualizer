"""Stock Visualizer Web Application

This Dash application serves as a dynamic platform for visualizing stock data, offering both historical and live stock information. 

Features:
- Two main tabs: 'Historical' and 'Live'.
- Historical Tab: Presents historical stock data using a Plotly graph and a transposed data table.
- Live Tab: Displays a live-updating Plotly graph, sourcing data from `quotes_publisher.py`.
"""

import asyncio
import dash
from dash import dcc, html
import modules.historical_tab as historical_tab
import modules.live_tab as live_tab
import quotes_publisher as quotes_publisher
from threading import Thread

app = dash.Dash(__name__)

# Set the layout for the app
app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Live', children=live_tab.get_layout()),
        dcc.Tab(label='Historical', children=historical_tab.get_layout())
    ])
])

# Register callbacks for live_tab
live_tab.register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True, port=8000)
