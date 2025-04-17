import time
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.core.config import settings

client = TestClient(app)

mocked_news_data = [
    {
        "category": "Neuroscience",
        "title": "Stem cells and Parkinson’s",
        "author": "Laura Sanders",
        "image_url": "https://example.com/image.jpg"
    }
]

@pytest.fixture
def fake_cache():
    return {
        settings.CACHE_KEY: (mocked_news_data, time.time())
    }

@patch("app.api.routes.news.fetch_trending_stories", return_value=mocked_news_data)
@patch("shelve.open")
def test_returns_cached_data(mock_shelve_open, mock_fetch_trending_stories, fake_cache):
    mock_shelf = MagicMock()
    mock_shelf.__enter__.return_value = fake_cache
    mock_shelve_open.return_value = mock_shelf

    response = client.get("/api/v1/trending-news")
    
    assert response.status_code == 200
    assert response.json() == mocked_news_data
    mock_fetch_trending_stories.assert_not_called()

@patch("app.api.routes.news.fetch_trending_stories", return_value=mocked_news_data)
@patch("shelve.open")
def test_refresh_forces_fetch(mock_shelve_open, mock_fetch_trending_stories):
    mock_shelf = {}
    shelve_mock = MagicMock()
    shelve_mock.__enter__.return_value = mock_shelf
    mock_shelve_open.return_value = shelve_mock

    response = client.get("/api/v1/trending-news?refresh=true")

    assert response.status_code == 200
    assert response.json() == mocked_news_data
    assert settings.CACHE_KEY in mock_shelf

@patch("app.api.routes.news.fetch_trending_stories", return_value=mocked_news_data)
@patch("shelve.open")
def test_expired_cache_fetches_fresh(mock_shelve_open, mock_fetch_trending_stories):
    old_time = time.time() - (settings.CACHE_TTL_SECONDS + 100)
    mock_cache = {
        settings.CACHE_KEY: (mocked_news_data, old_time)
    }
    mock_shelf = MagicMock()
    mock_shelf.__enter__.return_value = mock_cache
    mock_shelve_open.return_value = mock_shelf

    response = client.get("/api/v1/trending-news")

    assert response.status_code == 200
    assert response.json() == mocked_news_data
    mock_fetch_trending_stories.assert_called_once()

@patch("app.api.routes.news.fetch_trending_stories", side_effect=Exception("Something went wrong"))
@patch("shelve.open")
def test_handles_exception(mock_shelve_open, mock_fetch_trending_stories):
    mock_shelf = {}
    mock_context = MagicMock()
    mock_context.__enter__.return_value = mock_shelf
    mock_shelve_open.return_value = mock_context

    response = client.get("/api/v1/trending-news")

    assert response.status_code == 500
    assert response.json()["detail"] == settings.SERVER_ERROR_MESSAGE
