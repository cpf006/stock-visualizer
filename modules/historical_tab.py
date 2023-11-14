import pandas as pd
import plotly.graph_objs as go
from dash import html, dcc
import dash_bootstrap_components as dbc

def format_dataframe(df):
    """Formats the dataframe for display."""
    # Custom date parser to handle MMDDYYYY or MDDYYYY formats
    def parse_date(date_int):
        date_str = str(date_int)
        if len(date_str) == 7:  # MDDYYYY format
            date_str = '0' + date_str

        return pd.to_datetime(date_str, format='%m%d%Y')

    df['DATE'] = df['DATE'].apply(parse_date).dt.strftime('%Y-%m-%d')
    # Transpose the dataframe for the table
    df_transposed = df.set_index('DATE').T
    # Format numbers with dollar signs and two decimal points
    df_transposed = df_transposed.applymap(lambda x: f"${x:.2f}")
    return df, df_transposed

def create_time_series(df):
    """Creates a time series plot from the dataframe."""
    fig = go.Figure()
    for column in df.columns[1:]:  # Skip the first column (DATE)
        fig.add_trace(go.Scatter(x=df['DATE'], y=df[column], mode='lines', name=column))
    fig.update_layout(xaxis_title='Date', yaxis_title='Price')
    return fig

def get_layout():
    # Read and process the historical data
    df = pd.read_csv('data/stocks.csv')
    df, df_transposed = format_dataframe(df)

    # Create the graph
    graph = create_time_series(df)

    # Create the table
    table = dbc.Table.from_dataframe(df_transposed, striped=True, bordered=True, hover=True)

    # Combine into a layout
    layout = html.Div([
        dcc.Graph(id='historical-graph', figure=graph),
        html.Hr(),
        table
    ])

    return layout
