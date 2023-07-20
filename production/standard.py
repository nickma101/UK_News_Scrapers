from bs4 import BeautifulSoup
import feedparser, requests, json, os
from utils.utils import create_article
from datetime import datetime
from dateutil import parser
import re

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


# Define the default name and feed of the news outlet
NEWS_OUTLET = "EveningStandard"
NEWS_FEEDS = ["https://www.standard.co.uk/rss"]
NEWS_LANGUAGE = "en-UK"

date = datetime.utcnow()

# Read the RSS feed and retrieve URL and article metadata
def get_rss_feed(feed):
    article_list = []
    newsFeed = feedparser.parse(feed)

    for rss_article in newsFeed.entries:
        # Collection to hold the article specific metadata
        article_props = {}
        article_props['url'] = rss_article.link
        article_props['title'] = rss_article.title
        article_props['lead'] = rss_article.summary
        article_props['author'] = rss_article.author
        try:
            article_props['primaryCategory'] = rss_article.tags
        except:
            article_props['primaryCategory'] = "None"
        datestring = rss_article.published.split(" GMT")[0]
        published = parser.parse(datestring)
        article_props['date_published'] = published
        try:
            article_props['image'] = rss_article.media_content
        except:
            article_props['image'] = "None"
        article_props['date_updated'] = rss_article.updated

        article_list.append(article_props)

    return article_list


# Scrape individual articles and combine existing RSS meta-data with text from website
def scrape_article(article):
    response = requests.get(article['url'])
    soup = BeautifulSoup(response.content, 'html.parser')

    body = soup.find('div', {'id': 'main'}).text

    document = create_article(
        url=article['url'],
        primary_category=article['primaryCategory'][0]['term'],
        sub_categories="test",
        title=article['title'],
        lead=remove_html_tags(article['lead']),
        author=article['author'],
        date_published=article['date_published'],
        date_updated=article['date_updated'],
        language=NEWS_LANGUAGE,
        outlet=NEWS_OUTLET,
        image=article['image'][0]['url'],
        body=body
    )
    return document


# The scraper will retrieve news article URLs from the RSS feed and parse the HTML documents
def scrape():
    newsarticles_collection = []  # Collection to store complete articles

    for feed in NEWS_FEEDS:
        rss_results = get_rss_feed(feed)  # Get partial article information from RSS feeds
        for article in rss_results:
            try:
                new_article = scrape_article(article)

                if new_article:
                    newsarticles_collection.append(new_article)
            except Exception as e:
                print(f"Couldn't scrape article: {article['url']}")
    dateString = str(date)[:10]
    filename = "standard_articles" + dateString + ".json"
    desired_dir = "data"
    full_path = os.path.join(desired_dir, filename)

    with open(full_path, "w") as file:
        json.dump(newsarticles_collection, file, default=str)

    return newsarticles_collection

scrape()