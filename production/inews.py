from bs4 import BeautifulSoup
import requests
from utils.utils import create_article
from datetime import datetime, timedelta
import re

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
    title = soup.find('h1', {'class': 'headline'})
    lead = soup.find('h1', {'class': ' excerpt'})
    author = soup.find('div', {'class': 'author'})
    image = soup.find('img', {'class': 'w-100'})
    all_sorta_stuff = soup.find('div', {'class': 'article-content'})
    body = soup.find_all('p', all_sorta_stuff)
    published = soup.find('span', {'class': 'inews__post__pubdate'})
    updated = soup.find('span', {'class': 'inews__post__moddate'})

    document = create_article(
        url=url,
        primary_category="environment",
        sub_categories="test",
        title=title,
        lead=lead,
        author=author,
        date_published=published,
        date_updated=updated,
        language=NEWS_LANGUAGE,
        outlet=NEWS_OUTLET,
        image=image['src'],
        body=body
    )
    return document


def scrape_articles():
    articles = []
    urls = scrape_sitemap("https://inews.co.uk/category/news/environment")
    for url in urls:
        url = url.replace('"', '')
        article = scrape_article(url)
        articles.append(article)
    return articles


scrape_articles()
