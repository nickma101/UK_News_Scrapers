from bson.objectid import ObjectId
from datetime import datetime
import re

REMOVAL_WORDS = ["The BBC",                 # BBC identifier
                 "the BBC", 
                 "BBC", 
                 "BBC TV",
                 "The Guardian",            # Guardian identifier
                 "the Guardian", 
                 "Guardian",
                 "INews",                   # iNews identifier
                 "iNews",
                 "The Independent",         # Independent identifier
                 "the Independent", 
                 "Independent",
                 "The Evening Standard",    # Standard identifier
                 "the Evening Standard", 
                 "Evening Standard",
                 "Sky News"]                # Sky identifier
REPLACEMENT_WORD = "Informfully"

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
    body):
    return {
        "_id": generate_id(),                   # Generate custom ID because the backend uses strings instead of ObjectId()s
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

def clean_text(text):

    # Character replacement
    text = re.sub('[\“\”\‘\’]', '\'', text)
    text = re.sub('[\–\—]', '-', text)
    text = re.sub('[\ú\ü\ù\û]', 'u', text)
    text = re.sub('[è\é\ë\ê]', 'e', text)
    text = re.sub('[\à\è\á\â]', 'a', text)
    text = re.sub('[\í\ï\î]', 'i', text)
    text = re.sub('[\Ó\ô]', 'o', text)
    text = re.sub('[\ç]', 'c', text)

    # Spelling out
    text = re.sub('[\£]', 'GBP ', text)
    text = re.sub('[\€]', 'EUR ', text)
    text = re.sub('[\$]', 'USD ', text)
    text = re.sub('[\&]', 'and ', text)

    # dealing with weird sky news output
    text = re.sub('and #163;', 'GBP ', text)
    text = re.sub('and #160;', ' ', text)
    text = re.sub('and #8364;', 'EUR ', text)

    # Filtering out
    text = re.sub('[^a-zA-Z0-9 \.\,\(\)\!\?\:\;\%\-\+\#\@\'\n]', '', text)

    for word in REMOVAL_WORDS:
        text = text.replace(word, REPLACEMENT_WORD)

    return text
