#!/usr/bin/python
from credentials.creds import Guardian_api_key
import requests, json, os
from datetime import datetime, timedelta
from utils.utils import create_article

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
    "page-size": 200, #max allowed by the API
}


response = requests.get(base_url, params=query_params)

response_json = json.loads(response.text)


NEWS_LANGUAGE = 'en-UK'
NEWS_OUTLET = 'GuardianInt'

documentCollection = []

blacklist = ["crosswords"]

for article in response_json["response"]["results"]:

    if (article['sectionId'] not in blacklist) and ('corrections-and-clarifications' not in article['webUrl']) :

        try:
            datestring = article['webPublicationDate']
            datetime_obj = datetime.strptime(datestring, "%Y-%m-%dT%H:%M:%SZ")
            published = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
            document = create_article(
                    url=article['webUrl'],
                    primary_category=article['sectionId'],
                    sub_categories="test",
                    title=article['webTitle'],
                    lead=article['fields']['trailText'],
                    author=article['fields']['byline'],
                    date_published=published,
                    date_updated="test",
                    language=NEWS_LANGUAGE,
                    outlet=NEWS_OUTLET,
                    image=article['fields']['thumbnail'],
                    body=article['fields']['bodyText']
                )
            documentCollection.append(document)

        except:
            pass

    else:
        print(article['webUrl'])

dateString = str(date)[:10]
filename = "guardian_articles"+dateString+".json"
desired_dir = "data"
full_path = os.path.join(desired_dir, filename)

with open(full_path, "w") as file:
   json.dump(documentCollection, file, default=str)


