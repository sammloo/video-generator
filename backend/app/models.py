from pydantic import BaseModel, field_validator

class GenerateVideoRequest(BaseModel):
    text: str
    x: int
    y: int
    duration: int

    @field_validator('text')
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError("Text cannot be empty.")
        if len(v) > 255: 
            raise ValueError("Text must be less than or equal to 255 characters.")
        return v

    @field_validator('x')
    def validate_x(cls, v):
        if not (0 <= v <= 1920):
            raise ValueError("x must be between 0 and 1920.")
        return v

    @field_validator('y')
    def validate_y(cls, v):
        if not (0 <= v <= 1080):
            raise ValueError("y must be between 0 and 1080.")
        return v

    @field_validator('duration')
    def validate_duration(cls, v):
        if not (0 <= v <= 5):
            raise ValueError("Duration must be between 0 and 5.")
        return v

class GenerateAnimatedVideoRequest(BaseModel):
    text: str
    duration: int
    
    @field_validator('text')
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError("Text cannot be empty.")
        if len(v) > 255: 
            raise ValueError("Text must be less than or equal to 255 characters.")
        return v
    
    @field_validator('duration')
    def validate_duration(cls, v):
        if not (0 <= v <= 5):
            raise ValueError("Duration must be between 0 and 5.")
        return v

class TrendingStory(BaseModel):
    category: str
    title: str
    author: str
    image_url: str
    
class GenerateVideoResponse(BaseModel):
    status_code: int  
    status: str  
    video_id: str 
