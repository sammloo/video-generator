from app.core.config import settings
import shelve
import time
from app.models import TrendingStory
from typing import List
from fastapi import APIRouter, HTTPException, Query
from app.core.news import fetch_trending_stories
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/trending-news", response_model=List[TrendingStory])
def get_trending_news(refresh: bool = Query(False, description="Force re-scrape if true")):
    try:
        now = time.time()

        with shelve.open(settings.CACHE_FILE) as cache:
            if not refresh and settings.CACHE_KEY in cache:
                cached_data, timestamp = cache[settings.CACHE_KEY]
                if now - timestamp < settings.CACHE_TTL_SECONDS:
                    logger.info("Returned cached trending news.")
                    return cached_data

            results = fetch_trending_stories()
            cache[settings.CACHE_KEY] = (results, now)
            logger.info("Updated cache with fresh trending news.")
            return results

    except Exception as e:
        logger.error(f"Error fetching trending news: {e}")
        raise HTTPException(status_code=500, detail=settings.SERVER_ERROR_MESSAGE)