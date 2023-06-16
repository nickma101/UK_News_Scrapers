from bs4 import BeautifulSoup
import feedparser, requests, json, os
from utils.utils import create_article
from datetime import datetime
from dateutil import parser

# Define the default name and feed of the news outlet
NEWS_OUTLET = "SkyNews"
NEWS_FEEDS = [{'url': "https://feeds.skynews.com/feeds/rss/home.xml", 'category': "home"},
              {'url': "https://feeds.skynews.com/feeds/rss/uk.xml", 'category': "uk"},
              {'url':"https://feeds.skynews.com/feeds/rss/world.xml", 'category': "world"},
              {'url':"https://feeds.skynews.com/feeds/rss/business.xml", 'category': "business"},
              {'url':"https://feeds.skynews.com/feeds/rss/politics.xml", 'category': "politics"},
              {'url':"https://feeds.skynews.com/feeds/rss/technology.xml", 'category': "technology"},
              {'url':"https://feeds.skynews.com/feeds/rss/entertainment.xml", 'category': "entertainment"}]
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
        article_props['image'] = rss_article.media_content[0].get('url')

        article_list.append(article_props)

    return article_list

# Scrape individual articles and combine existing RSS meta-data with text from website
def scrape_article(article, category):
    response = requests.get(article['url'])
    soup = BeautifulSoup(response.content, 'html.parser')

    bodies = soup.find_all('div', {'data-component-name': 'sdc-article-body'})
    body = '<br/>'.join([str(b.text) for b in bodies])
    datestring = soup.find('p', {'class': 'sdc-article-date__date-time'}).text.split(',',1)[0]
    published = parser.parse(datestring)


    try:
        author = soup.find('span', {'class': 'sdc-article-author__name'}).text
    except:
        author = "None"

    document = create_article(
        url=article['url'],
        primary_category=category,
        sub_categories="test",
        title=article['title'],
        lead=article['lead'],
        author=author,
        date_published=published,
        date_updated="test",
        language=NEWS_LANGUAGE,
        outlet=NEWS_OUTLET,
        image=article['image'],
        body=body
    )
    return document


# The scraper will retrieve news article URLs from the RSS feed and parse the HTML documents
def scrape():
    newsarticles_collection = [] # Collection to store complete articles

    for e in NEWS_FEEDS:
        feed = e.get('url')
        category = e.get('category')
        rss_results = get_rss_feed(feed)  # Get partial article information from RSS feeds

        for article in rss_results:
            try:
                new_article = scrape_article(article, category)

                if new_article:
                    newsarticles_collection.append(new_article)
            except Exception as e:
                print(f"Couldn't scrape article: {article['url']}")
                print(e)

    dateString = str(date)[:10]
    filename = "sky_articles" + dateString + ".json"
    desired_dir = "data"
    full_path = os.path.join(desired_dir, filename)

    with open(full_path, "w") as file:
        json.dump(newsarticles_collection, file, default=str)

    return newsarticles_collection

scrape()