import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os
from main import app

client = TestClient(app)

def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

@patch("requests.get")
def test_weather_endpoint_success(mock_get):
    # Mock successful weather API response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "current_condition": [{
            "temp_C": "20",
            "weatherDesc": [{"value": "Sunny"}]
        }],
        "nearest_area": [{
            "areaName": [{"value": "London"}],
            "latitude": "51.5074",
            "longitude": "-0.1278"
        }]
    }
    mock_get.return_value = mock_response

    response = client.get("/weather?location=London")
    assert response.status_code == 200
    data = response.json()
    assert data["location"] == "London"
    assert data["temperature"] == "20"
    assert data["description"] == "Sunny"
    assert data["lat"] == 51.5074
    assert data["lon"] == -0.1278

@patch("requests.get")
def test_weather_endpoint_failure(mock_get):
    # Mock failed weather API response
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    response = client.get("/weather?location=InvalidLocation")
    assert response.status_code == 404


@patch.dict(os.environ, {"STRESS_TEST_FLAG": "true"})
def test_cpu_stress_invalid_params():
    # Test with invalid parameters
    response = client.get("/start_cpu_stress?duration=-1&load=50")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid duration or load parameter"

