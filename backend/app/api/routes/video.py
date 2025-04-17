from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from app.models import GenerateVideoRequest, GenerateAnimatedVideoRequest, GenerateVideoResponse
from app.core.video import create_video_with_text, create_video_with_animated_text
from app.utils import get_video_file_path
from app.core.config import settings
from app.utils import create_video_id
import logging
import os
import shelve
from fastapi import BackgroundTasks

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/generate_video", response_model=GenerateVideoResponse)
def generate_video(request: GenerateVideoRequest, background_tasks: BackgroundTasks):    
    video_id = create_video_id()
    with shelve.open(settings.CACHE_FILE) as cache:
        cache[video_id] = settings.TASK_STATUS["IN_PROGRESS"]
        
    background_tasks.add_task(
        create_video_with_text,
        video_id=video_id,
        text=request.text,
        position=(request.x, request.y),
        duration=request.duration
    )
    logger.info(f"Video generation started for text: {request.text}")
    response_data = GenerateVideoResponse(
        status_code=status.HTTP_200_OK,
        status="success",
        video_id=video_id,
    )
    return response_data


@router.post("/generate_animated_video", response_model=GenerateVideoResponse)
def generate_video(request: GenerateAnimatedVideoRequest, background_tasks: BackgroundTasks):    
    video_id = create_video_id()
    with shelve.open(settings.CACHE_FILE) as cache:
        cache[video_id] = settings.TASK_STATUS["IN_PROGRESS"]
        
    background_tasks.add_task(
        create_video_with_animated_text,
        video_id=video_id,
        text=request.text,
        duration=request.duration
    )
    logger.info(f"Video generation started for text: {request.text}")
    response_data = GenerateVideoResponse(
        status_code=status.HTTP_202_ACCEPTED,
        status="success",
        video_id=video_id,
    )
    return response_data


@router.get("/get_video")
def get_video(video_id: str):
    
    with shelve.open(settings.CACHE_FILE) as cache:
        status = cache.get(video_id, None)
        
    if status is None:
        raise HTTPException(status_code=404, detail="Task ID not found.")
        
    elif status == settings.TASK_STATUS["IN_PROGRESS"]:
        raise HTTPException(status_code=202, detail="Video generation is in progress.")
    
    elif status == settings.TASK_STATUS["FAILED"]:
        raise HTTPException(status_code=500, detail="Video generation failed.")
    
    video_file_path = get_video_file_path(video_id)
    try:
        logger.info("Successfully fetch video with Id {video_id}")
        return FileResponse(video_file_path, media_type="video/mp4")

    except Exception as e:
        logger.error(f"Error fetching video with ID {video_id}: {e}")
        raise HTTPException(status_code=500, detail=settings.SERVER_ERROR_MESSAGE)