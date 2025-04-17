# Video Generation Platform

## Overview

This a backend application for a Video Generation Platform, designed to perform basic video editing and include a scraping utility with caching.

**Tech Stack**: Python, FastAPI, Nginx, shelve

## Design decisions

- **FastAPI:** was chosen for its high performance and built-in support for async executions
- **Background Tasks:** was used to offload video generation to a background task and non-blocking
- **Shelve:** was picked for in-memory cache of trending stories and task status
- **Nginx:** was added to as a reverse proxy, and could serve static files, handle SSL, load balancing if needed.

## Features

- Create 5s video with text, supported changing text, duration and position
- Create 5s video with animated text from top-left to botton-right
- Scrape the last 10 trending stories with caching, return category, title, author, image URL.

## Setup

1. Clone the repository:

   ```sh
   git clone https://github.com/sammloo/video-generator.git
   cd video-generator
   ```

2. Start the backend using Docker:
   ```sh
   docker-compose up --build
   ```

## API Documentation

The backend provides a RESTful API. You can test the endpoints using Postman

### Example Endpoints:

- POST api/v1/generate_video
  ```sh
  {
      "text": "test",
      "x": 50,
      "y": 150,
      "duration": 5
  }
  ```
- POST api/v1/generate_animated_video

  ```sh
  {
     "text": "test",
     "duration": 3
  }
  ```

- GET api/v1/get_video?video_id=video-xxxxx
- GET api/v1/trending-news
- GET api/v1/trending-news?refresh=true

## Contact

For questions or issues, please create an issue in the repository.
