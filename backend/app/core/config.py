class Settings:
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "python challenge v2"
    
    VIDEO_SIZE = [1920, 1080]
    FONT_PATH = "app/static/montserrat-thin-2.ttf"
    BACKGROUND_IMAGE = "app/static/background.jpg"
    VIDEO_STORAGE_PATH = 'app/videos'
    VIDEO_DURATION = 5
    
    SERVER_ERROR_MESSAGE = "An error occurred while processing your request. Please try again later."
    
    CACHE_FILE = "/tmp/trending_cache.db"
    CACHE_KEY = "science_news"
    CACHE_TTL_SECONDS = 30
    
    TRENDING_NEWS_URL = "https://www.sciencenews.org/?s=&topic=&start-date=&end-date=&orderby=date"
    TASK_STATUS = {
        "IN_PROGRESS": "in_progress",
        "COMPLETED": "completed",
        "FAILED": "failed"
    }    
settings = Settings()