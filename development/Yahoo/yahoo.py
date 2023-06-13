from bs4 import BeautifulSoup
import feedparser, requests, json, os
from utils.utils import create_article
from datetime import datetime


# Define the default name and feed of the news outlet
NEWS_OUTLET = "Yahoo"
NEWS_FEED = "https://uk.news.yahoo.com/rss/"
NEWS_LANGUAGE = "en-UK"

date = datetime.utcnow()

# Read the RSS feed and retrieve URL and article metadata
def get_rss_feed():
    article_list = []
    newsFeed = feedparser.parse(NEWS_FEED)

    for rss_article in newsFeed.entries:
        print(rss_article)
        # Collection to hold the article specific metadata
        #print(rss_article)
        article_props = {}
        article_props['url'] = rss_article.link
        article_props['title'] = rss_article.title
        #article_props['lead'] = rss_article.description
        #article_props['author'] = rss_article.author
        #article_props['primaryCategory'] = rss_article.tags
        article_props['date_published'] = rss_article.published
        #article_props['image'] = rss_article.media_content

        article_list.append(article_props)

    return article_list


# Scrape individual articles and combine existing RSS meta-data with text from website
def scrape_article(article):
    response = requests.get(article['url'])
    soup = BeautifulSoup(response.content, 'html.parser')

    bodies = soup.find_all('p')
    body = '<br/>'.join([str(b.text) for b in bodies])

    sub_categories = "test"
    date_updated = "test"

    document = create_article(
        url=article['url'],
        primary_category="test",
        sub_categories="test",
        title=article['title'],
        lead="test",
        author="test",
        date_published=article['date_published'],
        date_updated=date_updated,
        language=NEWS_LANGUAGE,
        outlet=NEWS_OUTLET,
        image=article['image'][0]['url'],
        body=body
    )

    print(document)
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
    filename = "yahoo_articles" + dateString + ".json"
    desired_dir = "data"
    full_path = os.path.join(desired_dir, filename)

    with open(full_path, "w") as file:
        json.dump(newsarticles_collection, file, default=str)

    return newsarticles_collection

scrape()