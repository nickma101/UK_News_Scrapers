from bs4 import BeautifulSoup
import requests, json, re, os
from utils.utils import create_article
from datetime import datetime, timedelta

NEWS_OUTLET = "INews"
NEWS_LANGUAGE = "en-UK"
NEWS_FEEDS = ["https://inews.co.uk/category/news/environment", "https://inews.co.uk/category/news/politics",
              "https://inews.co.uk/category/news/sport", "https://inews.co.uk/category/news/money",
              "https://inews.co.uk/category/news/culture"]
date = datetime.utcnow()
yesterday = date - timedelta(days=1)


def scrape_sitemap(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news_posts = soup.find_all('div', {'class': 'inews__post-jot__content-headline'})
    # retrieve urls
    url_pattern = r'https?://\S+|www\.\S+'
    urls = re.findall(url_pattern, str(news_posts))
    return urls


def scrape_article(url):
    response = requests.get(url)
    # determine category
    if url != "http://www.w3.org/2000/svg><defs><clippath":
        pattern1 = r'/news/([^/]+)/'
        pattern2 = r'co.uk/([^/]+)/'
        try:
            category = re.findall(pattern1, url)[0]
        except:
            category = re.findall(pattern2, url)[0]
    else:
        category = "None"
    # reorganise categories
    if category == 'culture':
        category = 'entertainment&arts'
    if category == 'inews-lifestyle':
        category = 'lifeandstyle'
    soup = BeautifulSoup(response.content, 'html.parser')
    # scrape title
    try:
        title = soup.find('h1', {'class': 'headline'}).get_text()
    except:
        title = "None"
    # scrape lead
    lead = soup.find('h2').get_text()
    # scrape author
    authorbox = soup.find('div', {'class': 'inews__post-byline__author-link'})
    try:
        author = authorbox.find('a').get_text()
    except:
        author = "None"
    # scrape image
    image = soup.find('img', {'class': 'w-100'})
    try:
        image_src = image['src']
    except:
        image_src = "None"
    # scrape article body
    content = soup.find('div', {'class': 'article-content'})
    paragraphs = soup.find_all('p', content)
    for p in paragraphs:
        for a_tag in p.find_all('a'):
            a_tag.extract()
    body = []
    for p in paragraphs:
        if p.find('strong'):
            text = str(p.text).replace('INews', 'Informfully')
            body.append({"type": "headline", "text": text})
        else:
            text = str(p.text).replace('INews', 'Informfully')
            body.append({"type": "text", "text": text})
    # scrape date
    try:
        date_string = soup.find('span', {'class': 'inews__post__pubdate'}).get_text()
    except:
        date_string = date - timedelta(days = 10)
    date_format = "%B %d, %Y %I:%M %p"
    try:
        published = datetime.strptime(date_string, date_format)
    except:
        published = "None"
    try:
        updated = soup.find('span', {'class': 'inews__post__moddate'}).get_text()
    except:
        updated = 'None'
    #create article
    document = create_article(
        url=url,                                # string
        primary_category=category,              # string
        sub_categories="None",                  # string
        title=title,                            # string
        lead=lead,                              # string
        author=author,                          # string
        date_published=published,               # datetime
        date_updated=updated,                   # string            # NEEDS WORK BUT NECESSARY?
        language=NEWS_LANGUAGE,                 # string
        outlet=NEWS_OUTLET,                     # string
        image=image_src,                        # string
        body=body                               # list of dictionaries
    )
    return document


def scrape_articles():
    articles = []
    for feed in NEWS_FEEDS:
        urls = scrape_sitemap(feed)
        for url in urls:
            url = url.replace('"', '')
            article = scrape_article(url)
            # check if article is eligible for recommendation
            if len(article['body']) >= 7 and article['title'] != "None" and article["image"] != "None":
                articles.append(article)
    dateString = str(date)[:10]
    filename = "inews_articles" + dateString + ".json"
    desired_dir = "data"
    full_path = os.path.join(desired_dir, filename)

    with open(full_path, "w") as file:
        json.dump(articles, file, default=str)

    return articles


scrape_articles()
