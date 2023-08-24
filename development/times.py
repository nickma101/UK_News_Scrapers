from bs4 import BeautifulSoup
import requests, json, re, os
from utils.utils import create_article
from datetime import datetime, timedelta

NEWS_OUTLET = "INews"
NEWS_FEEDS = ["https://www.thetimes.co.uk/html-sitemap/"]
NEWS_LANGUAGE = "en-UK"
date = datetime.utcnow()
yesterday = date - timedelta(days=1)

def scrape_sitemap(url):
    # retrieve date and adjust format
    week = (yesterday.day - 1) // 7 + 1
    daily_date = str(yesterday)[:7] + "-" + str(week)
    daily_url = url + daily_date
    # retrieve articles and extract urls
    response = requests.get(daily_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news_posts = soup.find_all('li', {'class': 'Sitemap-link'})
    # retrieve urls
    urls = []
    for post in news_posts:
        link = post.find('a')
        urls.append("https://www.thetimes.co.uk"+link['href'])
    return urls

def scrape_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(url)
    # check if article is from yesterday
    try:
        date_box = soup.find('div', {'class' : 'tc-view__TcView-nuazoi-0 responsive__MetaContainer-cbxka9-3 FDabm'})
        published = date_box.find('time')['datetime'][:10]
    except:
        published = 'None'
    day_in_question = str(yesterday)[:10]
    if published == day_in_question:
        print('got one')
    else:
        print('not this one')
    try:
        title = soup.find('h1', {'class': 'responsive__HeadlineContainer-sc-15mjcnq-0 bXVomm'}).get_text()
    except:
        title = 'None'
    print(title)
    try:
        lead = soup.find('div', {'role': 'heading'}).get_text()
    except:
        lead = 'None'
    primary_category = soup.find('div', {'class': 'tc-text__TcText-sc-15igzev-0 kwFxdN'}).get_text()
    try:
        author = soup.find('a', {'class': 'tc-text-link__TcTextLink-sc-1voa8bp-0 text-link__LinkTextObj-xyehx2-0 vSslN'}).get_text()
    except:
        author = 'None'
    updated = published
    try:
        figure = soup.find('figure')
        image = figure.find('img')['src']
    except:
        image = 'None'
    bodies = soup.find_all('p', {'class': 'responsive__Paragraph-sc-1pktst5-0 gaEeqC'})
    print(bodies)
    body = 'test'

    document = create_article(
            url=url,                                # string
            primary_category=primary_category,      # string
            sub_categories="None",                  # string
            title=title,                            # string
            lead=lead,                              # string
            author=author,                          # string
            date_published=published,               # datetime
            date_updated=updated,                   # string            # NEEDS WORK BUT NECESSARY?
            language=NEWS_LANGUAGE,                 # string
            outlet=NEWS_OUTLET,                     # string
            image=image,                            # string
            body=body                               # list of dictionaries
        )
    return document

def scrape_articles():
    articles = []
    urls = scrape_sitemap("https://www.thetimes.co.uk/html-sitemap/")
    for url in urls:
        url = url.replace('"', '')
        article = scrape_article(url)
        articles.append(article)
    dateString = str(date)[:10]
    filename = "inews" + dateString + ".json"
    desired_dir = "../production/data"
    full_path = os.path.join(desired_dir, filename)

    with open(full_path, "w") as file:
        json.dump(articles, file, default=str)

    return articles


scrape_articles()