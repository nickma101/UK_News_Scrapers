from bs4 import BeautifulSoup
import feedparser
import requests
# from .utils.utils import create_article
from bson.objectid import ObjectId
from datetime import datetime
import json


def create_article(
        *,
        url,
        primary_category,
        sub_categories=[],
        title,
        lead,
        author=None,
        date_published,
        date_updated=None,
        language,
        outlet,
        image=None,
        body,
):
    return {
        "_id": generate_id(),  # Generate custom ID because the backend uses strings instead of ObjectId()s
        "url": url,
        "primaryCategory": primary_category,
        "subCategories": sub_categories,
        "title": title,
        "lead": lead,
        "author": author,
        "datePublished": date_published,
        "dateScraped": datetime.now(),
        "dateUpdated": date_updated,
        "language": language,
        "outlet": outlet,
        "image": image,
        "body": body,
    }


def generate_id():
    return str(ObjectId())


# Define the default name and feed of the news outlet
NEWS_OUTLET = "Independent"
NEWS_FEED = "https://www.independent.co.uk/news/uk/rss"
NEWS_LANGUAGE = "en-UK"

date = datetime.utcnow()

# Read the RSS feed and retrieve URL and article metadata
def get_rss_feed():
    article_list = []
    newsFeed = feedparser.parse(NEWS_FEED)

    for rss_article in newsFeed.entries:
        # Collection to hold the article specific metadata
        article_props = {}
        article_props['url'] = rss_article.link
        article_props['title'] = rss_article.title
        article_props['lead'] = rss_article.description
        article_props['author'] = rss_article.author
        article_props['primaryCategory'] = rss_article.tags
        article_props['date_published'] = rss_article.published
        article_props['image'] = rss_article.media_content

        article_list.append(article_props)

    return article_list


# Scrape individual articles and combine existing RSS meta-data with text from website
def scrape_article(article):
    response = requests.get(article['url'])
    soup = BeautifulSoup(response.content, 'html.parser')

    body = soup.find('div', {'id': 'main'}).text

    sub_categories = "test"
    date_updated = "test"

    document = create_article(
        url=article['url'],
        primary_category=article['primaryCategory'][0]['term'],
        sub_categories="test",
        title=article['title'],
        lead=article['lead'],
        author=article['author'],
        date_published=article['date_published'],
        date_updated=date_updated,
        language=NEWS_LANGUAGE,
        outlet=NEWS_OUTLET,
        image=article['image'][0]['url'],
        body=body
    )

    return document


# The scraper will retrieve news article URLs from the RSS feed and parse the HTML documents
def scrape():
    rss_results = get_rss_feed()  # Get partial article information from RSS feeds
    newsarticles_collection = []  # Collection to store complete articles

    for article in rss_results:
        try:
            new_article = scrape_article(article)

            if new_article:
                newsarticles_collection.append(new_article)
        except Exception as e:
            print(f"Couldn't scrape article: {article['url']}")
            print(e)
    dateString = str(date)[:10]
    filename = "independent_articles" + dateString + ".json"

    with open(filename, "w") as file:
        json.dump(newsarticles_collection, file, default=str)

    return newsarticles_collection

scrape()