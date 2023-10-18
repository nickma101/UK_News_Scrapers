from bs4 import BeautifulSoup
import feedparser, requests, json, os, re
from utils.utils import create_article
from datetime import datetime
from dateutil import parser

# Define the default name and feed of the news outlet
NEWS_OUTLET = "Independent"
NEWS_FEEDS = ["https://www.independent.co.uk/news/uk/rss",
              "https://www.independent.co.uk/climate-change/news/rss",
              "https://www.independent.co.uk/environment/rss",
              "https://www.independent.co.uk/sport/rss",
              "https://www.independent.co.uk/arts-entertainment/rss",
              "https://www.independent.co.uk/travel/rss",
              "https://www.independent.co.uk/life-style/rss"]
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
        article_props['lead'] = re.sub(r'<.*?>', '', rss_article.description)
        article_props['author'] = rss_article.author
        if hasattr(rss_article, 'tags'):
            article_props['primaryCategory'] = rss_article.tags
        else:
            article_props['primaryCategory'] = "None"
        datestring = rss_article.published.split(" GMT")[0]
        published = parser.parse(datestring)
        article_props['date_published'] = published
        if hasattr(rss_article, 'media_content'):
            article_props['image'] = rss_article.media_content
        else:
            article_props['image'] = "None"
        input_datetime = rss_article.updated
        parsed_datetime = datetime.strptime(input_datetime, "%Y-%m-%dT%H:%M:%S+00:00")
        formatted_datetime = parsed_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
        article_props['date_updated'] = formatted_datetime

        article_list.append(article_props)

    return article_list


# Scrape individual articles and combine existing RSS meta-data with text from website
def scrape_article(article):

    response = requests.get(article['url'])
    soup = BeautifulSoup(response.content, 'html.parser')

    # scrape article body
    divs = soup.find('div', {'class': 'sc-fwko30-0 dQSjZS main-wrapper'})
    all_paragraphs = []

    for div in divs:
        paragraphs = div.find_all('p')
        all_paragraphs.extend(paragraphs)

    filtered_paragraphs = [p for p in all_paragraphs]
    body = []

    for p in filtered_paragraphs:
        if "Read more:" not in p.text and "PA" not in p.text and "Want to bookmark your" not in p.text and "Read more from" not in p.text:
            if p.find('strong'):
                text = str(p.text).replace('\"', '"').replace('The Independent', 'Informfully').replace('Independent', 'Informfully')
                body.append({"type": "headline", "text": text})
            else:
                text = str(p.text).replace('/"', '"').replace('The Independent', 'Informfully').replace('Independent', 'Informfully')
                body.append({"type": "text", "text": text})

    # scrape category
    category = article['primaryCategory'][0]['term']

    # rename categories
    if category == 'Crime':
        category = 'crime'
    if category == 'Football':
        category = 'football'
    if category == 'Health &amp; Families':
        category = 'health'
    if category == 'Fashion' or category == 'Lofestyle':
        category = 'lifeandstyle'
    if category == 'UK Politics':
        category = 'politics'
    if category == 'Sport' or category == 'Cricket' or category == 'Golf':
        category = 'sport'
    if category == 'UK':
        category = 'uk news'

    document = create_article(
        url=article['url'],                                         # string
        primary_category=category,                                  # string
        sub_categories="None",                                      # string
        title=article['title'],                                     # string
        lead=article['lead'],                                       # string
        author=article['author'],                                   # string
        date_published=article['date_published'],                   # datetime
        date_updated=article['date_updated'],                       # datetime
        language=NEWS_LANGUAGE,                                     # string
        outlet=NEWS_OUTLET,                                         # string
        image=article['image'][0]['url'],                           # string
        body=body                                                   # list of dictionaries
    )

    return document


# The scraper will retrieve news article URLs from the RSS feed and parse the HTML documents
def scrape():

    # Collection to store complete articles
    newsarticles_collection = []

    # Get partial article information from RSS feeds
    for feed in NEWS_FEEDS:
        rss_results = get_rss_feed(feed)  # Get partial article information from RSS feeds
        retrieved_articles = 0
        skipped_articles = 0
        for article in rss_results:
            try:
                new_article = scrape_article(article)
                # check if article is eligible for recommendation
                if new_article and len(new_article['body']) >= 7 and new_article['image'] != "None":
                    newsarticles_collection.append(new_article)
                    retrieved_articles += 1
            except Exception as e:
                print(f"Couldn't scrape article: {article['url']}")
                print(e)
                skipped_articles += 1

    print(retrieved_articles, skipped_articles)

    dateString = str(date)[:10]
    filename = "independent_articles" + dateString + ".json"
    desired_dir = "data"
    full_path = os.path.join(desired_dir, filename)

    with open(full_path, "w") as file:
        json.dump(newsarticles_collection, file, default=str, ensure_ascii=False)

    return newsarticles_collection


scrape()
