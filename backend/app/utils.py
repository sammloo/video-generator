import uuid
import os
from app.core.config import settings

def create_video_id():
    return "video-" + str(uuid.uuid4())

def get_video_file_path(video_id):   
    return os.path.join(settings.VIDEO_STORAGE_PATH, f"{video_id}.mp4")