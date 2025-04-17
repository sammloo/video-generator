from moviepy import TextClip, CompositeVideoClip, ImageClip
from app.core.config import settings
from app.utils import get_video_file_path
import logging
import textwrap
import shelve

logger = logging.getLogger(__name__)

def create_video_with_text(video_id, text, position, duration):
    try:
        video_file_path = get_video_file_path(video_id)
        background = ImageClip(settings.BACKGROUND_IMAGE, duration=settings.VIDEO_DURATION)
        
        wrapped_text = "\n".join(textwrap.wrap(text, width=50)) 
        txt_clip = TextClip(text=wrapped_text, font_size=48, font=settings.FONT_PATH, color='white')
        txt_clip = txt_clip.with_position(position).with_duration(duration)

        video = CompositeVideoClip([background, txt_clip])
        video.write_videofile(video_file_path, fps=24)
        with shelve.open(settings.CACHE_FILE) as cache:
            cache[video_id] = settings.TASK_STATUS["COMPLETED"]
        logger.info(f"Video successfully saved at {video_file_path}")
    except Exception as e:
        with shelve.open(settings.CACHE_FILE) as cache:
            cache[video_id] = settings.TASK_STATUS["FAILED"]
        logger.error(f"Error during video creation: {e}")

def create_video_with_animated_text(video_id, text, duration):
    try:
        video_file_path = get_video_file_path(video_id)
        background = ImageClip(settings.BACKGROUND_IMAGE, duration=settings.VIDEO_DURATION)
        wrapped_text = "\n".join(textwrap.wrap(text, width=50))
        
        txt_clip = TextClip(text=wrapped_text, font_size=48, font=settings.FONT_PATH, color='black')
        
        def moving_position(t):
            width, height = settings.VIDEO_SIZE
            x_start, y_start = 50, 50
            x_end, y_end = width - 100, height - 100
            x = x_start + (x_end - x_start) * (t / duration)
            y = y_start + (y_end - y_start) * (t / duration)
            return (x, y)
        
        txt_clip = txt_clip.with_position(moving_position).with_duration(duration)

        video = CompositeVideoClip([background, txt_clip])
        video.write_videofile(video_file_path, fps=24)
        with shelve.open(settings.CACHE_FILE) as cache:
            cache[video_id] = settings.TASK_STATUS["COMPLETED"]
        logger.info(f"Video successfully saved at {video_file_path}")
    except Exception as e:
        with shelve.open(settings.CACHE_FILE) as cache:
            cache[video_id] = settings.TASK_STATUS["FAILED"]
        logger.error(f"Error during video creation: {e}")

