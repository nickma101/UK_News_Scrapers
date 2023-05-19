
import requests
import json
from datetime import datetime, timedelta


api_key = "4ed35a9f-ee74-47db-8cc6-0aac0a181417"
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


def create_article(
    url,
    primary_category,
    #sub_categories = [],
    title,
    lead,
    author,
    date_published,
    #date_updated = None,
    language,
    outlet,
    image,
    body,
):

    return {
        "url": url,
        "primaryCategory": primary_category,
        #"subCategories": sub_categories,
        "title": title,
        "lead": lead,
        "author": author,
        "datePublished": date_published,
        "dateScraped": datetime.now(),
        #"dateUpdated": date_updated,
        "language": language,
        "outlet": outlet,
        "image": image,
        "body": body,
    }


NEWS_LANGUAGE = 'en-UK'
NEWS_OUTLET = 'GuardianInt'

documentCollection = []

blacklist = ["crosswords"]

for article in response_json["response"]["results"]:

    if (article['sectionId'] not in blacklist) and ('corrections-and-clarifications' not in article['webUrl']) :

        try:
            document = create_article(
                    url=article['webUrl'],
                    primary_category=article['sectionId'],
                    #sub_categories=sub_categories,
                    title=article['webTitle'],
                    lead=article['fields']['trailText'],
                    author=article['fields']['byline'],
                    date_published=article['webPublicationDate'],
                    #date_updated=modify_date,
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

print(documentCollection)
