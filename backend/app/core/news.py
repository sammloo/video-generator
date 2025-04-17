
import requests
from app.core.config import settings
import logging
from bs4 import BeautifulSoup
from app.models import TrendingStory
import re

logger = logging.getLogger(__name__)

def fetch_trending_stories():
    response = requests.get(settings.TRENDING_NEWS_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    story_blocks = soup.find_all("li", class_=re.compile(r"post-item-river__wrapper"))
    results = []

    for block in story_blocks[:10]:
        
        category_tag = block.find("a", class_=re.compile(r"post-item-river__eyebrow"))
        category = category_tag.text.strip() if category_tag else "Unknown"

        title_tag = block.find("h3", class_=re.compile(r"post-item-river__title"))
        title_link = title_tag.find("a") if title_tag else None
        title = title_link.text.strip() if title_link else "Untitled"

        author_tag = block.find("a", class_="byline-link")
        author = author_tag.text.strip() if author_tag else "Unknown"

        img_tag = block.find("img")
        image_url = img_tag["src"] if img_tag and img_tag.has_attr("src") else ""

        results.append(TrendingStory(
            category=category,
            title=title,
            author=author,
            image_url=image_url
        ))

    return results