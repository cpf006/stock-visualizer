import pytest
from modules import historical_tab
import pandas as pd
from dash import dcc, dash_table

sample_data = {
    'DATE': ['12012021', '6012023'],  # Example dates
    'STK1': [137.76, 138],            # Example stock data
    'STK2': [92.86, 92.5]             # Additional stock data
}

@pytest.fixture
def sample_dataframe():
    """Fixture to create a sample dataframe for testing."""
    return pd.DataFrame(sample_data)

def test_format_dataframe(sample_dataframe):
    """Test the formatting of the dataframe."""
    formatted_df, df_transposed = historical_tab.format_dataframe(sample_dataframe)

    # Check if DATE column is formatted correctly
    assert all(formatted_df['DATE'] == ['2021-12-01', '2023-06-01']), "Date formatting is incorrect"
    assert df_transposed.shape == (2, 3), "Dataframe transposition is incorrect"

def test_create_time_series(sample_dataframe):
    """Test the creation of the time series plot."""
    formatted_df, _ = historical_tab.format_dataframe(sample_dataframe)
    fig = historical_tab.create_time_series(formatted_df)
    
    # Check if the figure is created with correct titles
    assert fig.layout.xaxis.title.text == 'Date', "X-axis title is incorrect"
    assert fig.layout.yaxis.title.text == 'Price', "Y-axis title is incorrect"
    
    # Check if data is correctly plotted
    assert len(fig.data) == len(sample_dataframe.columns) - 1, "Incorrect number of traces in the plot"

def test_get_layout():
    """Test the layout creation for the historical tab."""
    layout = historical_tab.get_layout()
    assert any(isinstance(component, dcc.Graph) for component in layout.children), "Graph component missing in layout"
    assert any(isinstance(component, dash_table.DataTable) for component in layout.children), "DataTable component missing in layout"
