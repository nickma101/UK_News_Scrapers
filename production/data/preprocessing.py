from datetime import datetime
import json

#setting the current date
now = datetime.utcnow()
date = now.strftime('%Y-%m-%d')

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
    return articles

def get_articles():
    data = get_data()
    articles = []
    for d in data:
        #some preprocessing
        articles.append(d)
    return articles

get_data()



