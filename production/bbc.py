from bs4 import BeautifulSoup
import feedparser, requests, json, os
from utils.utils import create_article
from datetime import datetime
from dateutil import parser


# Define the default name and feed of the news outlet
NEWS_OUTLET = "BBC"
NEWS_FEEDS = ["http://feeds.bbci.co.uk/news/rss.xml", "http://feeds.bbci.co.uk/news/world/rss.xml", "http://feeds.bbci.co.uk/news/business/rss.xml", "http://feeds.bbci.co.uk/news/technology/rss.xml", "http://feeds.bbci.co.uk/news/politics/rss.xml", "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml", "http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml", "http://feeds.bbci.co.uk/news/health/rss.xml"]
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
        try:
            article_props['lead'] = rss_article.summary
        except:
            article_props['lead'] = "Click here to read more"
        datestring = rss_article.published.split(" GMT")[0]
        published = parser.parse(datestring)
        article_props['date_published'] = published
        article_list.append(article_props)

    return article_list

# Scrape individual articles and combine existing RSS meta-data with text from website
def scrape_article(article):
    response = requests.get(article['url'])
    soup = BeautifulSoup(response.content, 'html.parser')

    bodies = soup.findAll({'p': {'data-component': 'text-block'}})
    body = '<br/>'.join([str(b.text) for b in bodies])
    categories = soup.find_all('li', {'class': 'ssrcss-shgc2t-StyledMenuItem eis6szr3'})
    primary_category = categories[0].text
    sub_categories = ','.join([str(c.text) for c in categories[1:]])
    image = soup.find('img').get("src")
    try:
        author = soup.find('div', {'class': 'ssrcss-68pt20-Text-TextContributorName e8mq1e96'}).text
    except:
        author = "No author"

    date_updated = "test"

    document = create_article(
        url=article['url'],
        primary_category=primary_category,
        sub_categories=sub_categories,
        title=article['title'],
        lead=article['lead'],
        author=author,
        date_published=article['date_published'],
        date_updated=date_updated,
        language=NEWS_LANGUAGE,
        outlet=NEWS_OUTLET,
        image=image,
        body=body
    )
    return document


# The scraper will retrieve news article URLs from the RSS feed and parse the HTML documents
def scrape():
    newsarticles_collection = [] # Collection to store complete articles
    for feed in NEWS_FEEDS:
        rss_results = get_rss_feed(feed) # Get partial article information from RSS feeds
        for article in rss_results:
            try:
                new_article = scrape_article(article)
                if new_article:
                    newsarticles_collection.append(new_article)
            except Exception as e:
                print(f"Couldn't scrape article: {article['url']}")
                print(e)

    dateString = str(date)[:10]
    filename = "bbc_articles" + dateString + ".json"
    desired_dir = "data"
    full_path = os.path.join(desired_dir, filename)

    with open(full_path, "w") as file:
        json.dump(newsarticles_collection, file, default=str)
    return newsarticles_collection

scrape()