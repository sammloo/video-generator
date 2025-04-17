import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.core.config import settings

client = TestClient(app)

@pytest.fixture
def video_id():
    return "test123"

def test_generate_video_success(video_id):
    payload = {
        "text": "Hello world",
        "x": 100,
        "y": 150,
        "duration": 5
    }

    with patch("app.api.routes.video.create_video_with_text", return_value=video_id):
        response = client.post("/api/v1/generate_video", json=payload)

    assert response.status_code == 200
    assert response.json() == {
        "status_code": 200,
        "status": "success",
        "video_id": video_id
    }

def test_generate_video_file_not_found():
    payload = {
        "text": "Missing font test",
        "x": 50,
        "y": 100,
        "duration": 5
    }

    with patch("app.api.routes.video.create_video_with_text", side_effect=FileNotFoundError("Font not found")):
        response = client.post("/api/v1/generate_video", json=payload)

    assert response.status_code == 400
    assert "Required font or file is missing" in response.text

def test_generate_animated_video_success(video_id):
    payload = {
        "text": "Animated Text",
        "duration": 5
    }

    with patch("app.api.routes.video.create_video_with_animated_text", return_value=video_id):
        response = client.post("/api/v1/generate_animated_video", json=payload)

    assert response.status_code == 200
    assert response.json()["video_id"] == video_id

def test_get_video_success(tmp_path):
    video_id = "dummy_video"
    video_file = tmp_path / f"{video_id}.mp4"
    video_file.write_bytes(b"fake video content")

    with patch("app.api.routes.video.get_video_file_path", return_value=str(video_file)):
        response = client.get(f"/api/v1/get_video?video_id={video_id}")
        assert response.status_code == 200
        assert response.headers["content-type"] == "video/mp4"

def test_get_video_not_found(video_id):
    with patch("app.api.routes.video.get_video_file_path", return_value=f"/tmp/{video_id}.mp4"), \
         patch("os.path.exists", return_value=False):
        
        response = client.get(f"/api/v1/get_video?video_id={video_id}")
        assert response.status_code == 404
        assert "Requested video does not exist" in response.text
