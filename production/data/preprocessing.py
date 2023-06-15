from datetime import datetime
import json

#what to include / exclude
topics = []
min-length = 500
date = datetime.utcnow().strftime('%Y-%m-%d')


#retrieveing the daily data
def get_data():
    outlets = ["bbc", "guardian", "independent", "sky"]
    articles = []
    for outlet in outlets:
        try:
            file = outlet+"_articles"+date+".json"
            data = open(file)
            articles = json.load(data)
        except:
            print('no articles today it seems')
    for article in articles:
        #some preprocessing, including:
        # standardising datetimes
        # standardising topics
    return articles

def get_articles():
    data = get_data()
    articles = []
    for d in data:
        #some filtering, including:
        # filtering out short texts
        # filtering out old articles
        # filtering out unwanted topics
        articles.append(d)
    return articles

get_data()



