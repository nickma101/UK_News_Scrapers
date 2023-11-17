from bson.objectid import ObjectId
from datetime import datetime
import re

def generate_id():
    return str(ObjectId())

def create_article(
    *,
    url,
    primary_category,
    sub_categories = [],
    title,
    lead,
    author = None,
    date_published,
    date_updated = None,
    language,
    outlet,
    image = None,
    body,
):
    return {
        "_id": generate_id(), # Generate custom ID because the backend uses strings instead of ObjectId()s
        "url": url,
        "articleType": "text",
        "primaryCategory": primary_category,
        "subCategories": sub_categories,
        "title": title,
        "lead": lead,
        "author": author,
        "datePublished": datetime.now(),
        "dateScraped": datetime.now(),
        "dateUpdated": datetime.now(),
        "language": language,
        "outlet": outlet,
        "image": image,
        "body": body,
    }

def cleanText(text):
    # TODO Replace exotic quotation marks...
    return re.sub('[^a-zA-Z0-9 \n\.\£\$\!\?\'\:\;\%\€]', '', text)
