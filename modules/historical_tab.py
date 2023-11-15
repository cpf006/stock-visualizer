import pandas as pd
import plotly.graph_objs as go
from dash import html, dcc, dash_table


def format_dataframe(df):
    """Formats the dataframe for display."""

    def parse_date(date_int):
        date_str = str(date_int)
        if len(date_str) == 7:  # MDDYYYY format
            date_str = "0" + date_str
        return pd.to_datetime(date_str, format="%m%d%Y")

    df["DATE"] = df["DATE"].apply(parse_date).dt.strftime("%Y-%m-%d")

    # Transpose the dataframe for the table
    df_transposed = df.set_index("DATE").T
    df_transposed.reset_index(inplace=True)
    df_transposed.rename(columns={"index": "Date"}, inplace=True)

    # Format numbers with dollar signs and two decimal points
    df_transposed = df_transposed.applymap(
        lambda x: f"${x:.2f}" if isinstance(x, (int, float)) else x
    )

    return df, df_transposed


def create_time_series(df):
    """Creates a time series plot from the dataframe."""
    fig = go.Figure()
    for column in df.columns[1:]:  # Skip the first column (DATE)
        fig.add_trace(go.Scatter(x=df["DATE"], y=df[column], mode="lines", name=column))
    fig.update_layout(xaxis_title="Date", yaxis_title="Price")
    return fig


def get_layout():
    # Read and process the historical data
    df = pd.read_csv("data/stocks.csv")
    df, df_transposed = format_dataframe(df)

    # Create the graph
    graph = create_time_series(df)

    # Create the DataTable
    data = df_transposed.to_dict("records")
    columns = [{"name": col, "id": col} for col in df_transposed.columns]

    table = dash_table.DataTable(
        data=data,
        columns=columns,
        style_table={"overflowY": "auto", "height": "300px"},
        style_header={"backgroundColor": "lightgrey", "fontWeight": "bold"},
        style_cell={
            "textAlign": "left",
            "backgroundColor": "white",
            "border": "1px solid black",
        },
        style_data_conditional=[
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "white",
            }
        ],
        row_deletable=False,
        editable=False,
        sort_action="native",
        filter_action="native",
    )

    # Combine into a layout
    layout = html.Div([dcc.Graph(id="historical-graph", figure=graph), table])

    return layout
