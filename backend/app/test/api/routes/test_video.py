import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.core.config import settings

client = TestClient(app)

    
def test_generate_video_success():
    payload = {
        "text": "Video Success Test",
        "x": 100,
        "y": 150,
        "duration": 5
    }

    with patch("app.api.routes.video.create_video_id", return_value="test_generate_video"):
        response = client.post("/api/v1/generate_video", json=payload)

    assert response.status_code == 200
    assert response.json() == {
        "status_code": 200,
        "status": "success",
        "video_id": "test_generate_video"
    }

def test_generate_video_file_failed():
    payload = {
        "text": "Missing font test",
        "x": 50,
        "y": 100,
        "duration": 5
    }
    with patch("app.core.video.TextClip", side_effect=FileNotFoundError("Font not found")), \
         patch("app.api.routes.video.create_video_id", return_value="test_generate_video_failed"):
        response = client.post("/api/v1/generate_video", json=payload)

    assert response.status_code == 200

def test_generate_animated_video_success():
    payload = {
        "text": "Animated Video Test",
        "duration": 5
    }

    with patch("app.api.routes.video.create_video_id", return_value="test-generate-animated-video"):
        response = client.post("/api/v1/generate_animated_video", json=payload)

    assert response.status_code == 200
    
def test_get_video_success():
    response = client.get(f"/api/v1/get_video?video_id=test_generate_video")
    assert response.status_code == 200
    assert response.headers["content-type"] == "video/mp4"

def test_get_video_failed():
    response = client.get(f"/api/v1/get_video?video_id=test_generate_video_failed")
    assert response.status_code == 500
    assert "Video generation failed" in response.text

def test_get_animated_video_success():
    response = client.get(f"/api/v1/get_video?video_id=test-generate-animated-video")
    assert response.status_code == 200
    assert response.headers["content-type"] == "video/mp4"