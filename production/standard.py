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
    # scrape article text
    divs = soup.find('div', {'class': 'sc-enDNfw iLaNIc'})
    paragraphs = []
    #first_letter = divs.find('span').text
    if divs:
        # Find all 'div' elements with class 'sc-kxZkPw kMnNar' and remove them
        for unwanted_div in divs.find_all('div', {'class': 'sc-kxZkPw kMnNar'}):
            unwanted_div.extract()

        # Find and add all 'p' and 'h2' tags within the modified 'divs' element
        block = divs.find_all(['p', 'h2'])
        paragraphs.extend(block)
    # for div in divs:
    #     if div.find('div', {'class': 'sc-kxZkPw kMnNar'}):
    #     block = div.find_all(['p', 'h2'])
    #    paragraphs.extend(block)
    body = []
    #first_paragraph = paragraphs[0]
    #body.append({"type": "text", "text": str(first_letter) + str(first_paragraph.text)})
    #other_paragraphs = paragraphs[1:]
    for p in paragraphs:
        if ("Read more:" not in p.text and
                "Sign up for exclusive newsletters" not in p.text and
                "By clicking Sign up you confirm that" not in p.text and
                "MORE ABOUT" not in p.text and
                "Have your say..." not in p.text and
                "This site is protected by reCAPTCHA" not in p.text):
            if p.get_text().startswith('"') and p.get_text().endswith('"'):
                # If the text starts and ends with double quotation marks, treat it as a quote
                cleaned_text = p.get_text().replace('"', "'")
                body.append({"type": "quote", "text": cleaned_text})
            elif p.name == 'h2':
                cleaned_text = p.get_text().replace('"', "'")
                body.append({"type": "headline", "text": cleaned_text})
            else:
                cleaned_text = str(p.text).replace('The Standard', 'Informfully').replace('"', "'")
                body.append({"type": "text", "text": cleaned_text})
    # scrape category
    category = article['primaryCategory'][0]['term']
    # rename categories
    if category == 'Business' or category == 'Business News':
        category = 'business'
    if category == 'Crime':
        category = 'crime'
    if category == 'Environment':
        category = 'environment'
    if category == 'Film' or category == 'Music' or category == 'Showbiz' or category == 'Celebrity News':
        category = 'entertainment&arts'
    if category == 'Football':
        category = 'football'
    if category == 'Health':
        category = 'health'
    if category == 'Fashion' or category == 'Lifestyle':
        category = 'lifeandstyle'
    if category == 'Money':
        category = 'money'
    if category == 'Politics':
        category = 'politics'
    if category == 'Boxing' or category == 'Golf' or category == 'F1':
        category = 'sport'
    if category == 'Science':
        category = 'science'
    if category == 'Tech':
        category = 'technology'
    if category == 'UK':
        category = 'uk news'
    if category == 'World':
        category = 'world'
    # create article
    document = create_article(
        url=article['url'],                                         # string
        primary_category=category,     # string
        sub_categories="None",                                      # string
        title=article['title'],                                     # string
        lead=remove_html_tags(article['lead']),                     # string
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
    newsarticles_collection = []  # Collection to store complete articles
    retrieved_articles = 0
    skipped_articles = 0

    for feed in NEWS_FEEDS:
        rss_results = get_rss_feed(feed)  # Get partial article information from RSS feeds
        for article in rss_results:
            try:
                new_article = scrape_article(article)
                # check if article is eligible for recommendation
                if new_article and len(new_article['body']) >= 7:
                    newsarticles_collection.append(new_article)
                    retrieved_articles += 1
            except Exception as e:
                print(f"Couldn't scrape article: {article['url']}")
                print(e)
                skipped_articles += 1

    print(retrieved_articles, skipped_articles)


    dateString = str(date)[:10]
    filename = "standard_articles" + dateString + ".json"
    desired_dir = "data"
    full_path = os.path.join(desired_dir, filename)

    with open(full_path, "w") as file:
        json.dump(newsarticles_collection, file, default=str, ensure_ascii=False)

    return newsarticles_collection


scrape()
