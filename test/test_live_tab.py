import pytest
from dash import dcc
from dash.exceptions import PreventUpdate
from modules import live_tab
import json

sample_json_data = json.dumps({
    "STK1": [137.76, 138],
    "STK2": [92.86, 92.5],
    "TIMESTAMP": [1, 2]
})

def test_get_layout():
    """Test the layout creation for the live tab."""
    layout = live_tab.get_layout()
    assert any(isinstance(component, dcc.Graph) for component in layout.children), "Graph component missing in layout"

def test_store_data():
    """Test the store_data callback function."""
    updated_data = live_tab.store_data(sample_json_data, None)
    assert updated_data is not None, "Data should not be None"
    assert updated_data == json.loads(sample_json_data), "Stored data should match the input JSON"

def test_update_graph():
    """Test the update_graph callback function."""
    existing_figure = None
    n_intervals = 0
    json_data = json.loads(sample_json_data)  # Parse JSON string to dictionary

    # Simulate the callback with sample data
    with pytest.raises(PreventUpdate):
        live_tab.update_graph(n_intervals, None, existing_figure)

    updated_figure = live_tab.update_graph(n_intervals, json_data, existing_figure)
    assert "data" in updated_figure, "Figure should have data"
    assert len(updated_figure["data"]) > 0, "Figure data should not be empty"