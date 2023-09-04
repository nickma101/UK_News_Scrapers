from bs4 import BeautifulSoup
import requests, json, re, os
from utils.utils import create_article
from datetime import datetime, timedelta

NEWS_OUTLET = "INews"
NEWS_FEEDS = ["https://inews.co.uk/category/news/environment"]
NEWS_LANGUAGE = "en-UK"
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
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('h1', {'class': 'headline'}).get_text()
    lead = soup.find('h2').get_text()
    authorbox = soup.find('div', {'class': 'inews__post-byline__author-link'})
    author = authorbox.find('a').get_text()
    image = soup.find('img', {'class': 'w-100'})
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
    date_string = soup.find('span', {'class': 'inews__post__pubdate'}).get_text()
    date_format = "%B %d, %Y %I:%M %p"
    published = datetime.strptime(date_string, date_format)
    try:
        updated = soup.find('span', {'class': 'inews__post__moddate'}).get_text()
    except:
        updated = 'None'

    document = create_article(
        url=url,                                # string
        primary_category="environment",         # string
        sub_categories="None",                  # string
        title=title,                            # string
        lead=lead,                              # string
        author=author,                          # string
        date_published=published,               # datetime
        date_updated=updated,                   # string            # NEEDS WORK BUT NECESSARY?
        language=NEWS_LANGUAGE,                 # string
        outlet=NEWS_OUTLET,                     # string
        image=image['src'],                     # string
        body=body                               # list of dictionaries
    )
    return document


def scrape_articles():
    articles = []
    urls = scrape_sitemap("https://inews.co.uk/category/news/environment")
    for url in urls:
        url = url.replace('"', '')
        article = scrape_article(url)
        articles.append(article)
    dateString = str(date)[:10]
    filename = "inews" + dateString + ".json"
    desired_dir = "data"
    full_path = os.path.join(desired_dir, filename)

    with open(full_path, "w") as file:
        json.dump(articles, file, default=str)

    return articles


scrape_articles()
