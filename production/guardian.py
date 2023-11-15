#!/usr/bin/python
from credentials.creds import Guardian_api_key
import requests, json, os
from datetime import datetime, timedelta
from utils.utils import create_article
from bs4 import BeautifulSoup
from bson import json_util

api_key = Guardian_api_key
base_url = "https://content.guardianapis.com/search"
date = datetime.utcnow()
yesterday = date - timedelta(days=1)

query_params = {
    "api-key": api_key,
    "orderBy": "newest",
    "show-fields": "all",
    "show-tags": "all",
    "from-date": yesterday.date().isoformat(),
    "to-date": date.date().isoformat(),
    "page-size": 200,                               # max allowed by the API
}

NEWS_LANGUAGE = 'en-UK'
NEWS_OUTLET = 'GuardianInt'
DEFAULT_AUTHOR = 'None'

blacklist = ["crosswords", '/live']

response = requests.get(base_url, params=query_params)
response_json = json.loads(response.text)

def scrape():
    newsarticles_collection = []

    retrieved_articles = 0
    skipped_articles = 0
    for article in response_json["response"]["results"]:

        if (article['sectionId'] not in blacklist) and ('corrections-and-clarifications' not in article['webUrl']):
            try:
                datestring = article['webPublicationDate']
                datetime_obj = datetime.strptime(datestring, "%Y-%m-%dT%H:%M:%SZ")
                published = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
                category = article['sectionId']
                # reorganise categories
                if category == 'fashion':
                    category = 'lifeandstyle'
                if category == 'artanddesign' or category == 'film' or category == 'music' or category == 'culture':
                    category = 'entertainment&arts'
                # scrape author
                if 'byline' in article['fields']:
                    author = article['fields']['byline']
                else:
                    author = DEFAULT_AUTHOR
                # scrape body text and save as dictionary
                soup = BeautifulSoup(article['fields']['body'], 'html.parser')
                all_paragraphs = []
                for e in soup.find_all('p'):
                    all_paragraphs.append(e)
                filtered_paragraphs = [p for p in all_paragraphs if not p.has_attr('class')]
                body = []
                for p in filtered_paragraphs:
                    if "Read more:" not in p.text and "Related:" not in p.text:
                        if p.find('strong'):
                            text = str(p.text).replace('The Guardian', 'Informfully').replace('“', "'").replace('”', "'").replace('‘', "'").replace('’', "'").replace("’", "'")
                            body.append({"type": "headline", "text": text})
                        else:
                            text = str(p.text).replace('The Guardian', 'Informfully').replace('“', "'").replace('”', "'").replace('‘', "'").replace('’', "'").replace("’", "'")
                            if text.startswith("'") and text.endswith("'"):
                                body.append({"type": "quote", "text": text})
                            else:
                                body.append({"type": "text", "text": text})
                        # create article
                        document = create_article(
                            url=article['webUrl'],                  # string
                            primary_category=category,              # string
                            sub_categories="None",                  # string
                            title=article['webTitle'],              # string
                            lead=article['fields']['trailText'],    # string
                            author=author,                          # string
                            date_published=published,               # datetime
                            date_updated=published,                 # datetime NEEDS WORK
                            language=NEWS_LANGUAGE,                 # string
                            outlet=NEWS_OUTLET,                     # string
                            image=article['fields']['thumbnail'],   # string
                            body=body                               # list of dictionaries
                        )
                # filter out short articles
                if len(body) >= 7 and '/live' not in document['url']:
                    newsarticles_collection.append(document)
                    retrieved_articles += 1
                else:
                    skipped_articles += 1
                    pass
            except:
                pass

        else:
            print(article['webUrl'])

    print(retrieved_articles, skipped_articles)

    dateString = str(date)[:10]
    filename = "guardian_articles" + dateString + ".json"
    desired_dir = "data"
    full_path = os.path.join(desired_dir, filename)

    with open(full_path, "w") as file:
        json.dump(newsarticles_collection, file, default=json_util.default, ensure_ascii=False)

    return newsarticles_collection

scrape()


