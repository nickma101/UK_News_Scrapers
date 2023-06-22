from datetime import datetime, timedelta
import json

# what to include / exclude
topics = ["business", "crime", "entertainment", "football", "health", "lifestyle", "politics", "science", "sport",
          "technology", "travel", "uk_news", "world"]
minLength = 2000
#date = datetime.utcnow().strftime('%Y-%m-%d')
dates = [ '2023-06-22', '2023-06-21', '2023-06-20', '2023-06-19', '2023-06-16', '2023-06-15', '2023-06-14', '2023-06-13']
today = datetime.utcnow()
yesterday = today - timedelta(days=1)

# retrieving the daily data
def get_data():
    outlets = ["bbc", "guardian", "independent", "sky", "guardian_environment"]
    all_articles = []
    # read in data
    for date in dates:
        for outlet in outlets:
            try:
                file = outlet+"_articles"+date+".json"
                data = open(file)
                articles = json.load(data)
            except:
                print('no articles today it seems')
            # standardise topics
            for article in articles:
                # business
                if article.get('primaryCategory') == "Business":
                    article.update({'primaryCategory': "business"})
                # crime
                if article.get('primaryCategory') == "Crime":
                    article.update({'primaryCategory': "crime"})
                # entertainment
                if article.get('primaryCategory') == "Entertainment & Arts":
                    article.update({'primaryCategory': "entertainment"})
                if article.get('primaryCategory') == "books":
                    article.update({'primaryCategory': "entertainment"})
                if article.get('primaryCategory') == "culture":
                    article.update({'primaryCategory': "entertainment"})
                if article.get('primaryCategory') == "film":
                    article.update({'primaryCategory': "entertainment"})
                if article.get('primaryCategory') == "music":
                    article.update({'primaryCategory': "entertainment"})
                # football
                if article.get('primaryCategory') == "Football":
                    article.update({'primaryCategory': "football"})
                # health
                if article.get('primaryCategory') == "Health":
                    article.update({'primaryCategory': "health"})
                if article.get('primaryCategory') == "Health &amp; Families":
                    article.update({'primaryCategory': "health"})
                # lifestyle
                if article.get('primaryCategory') == "Lifestyle":
                    article.update({'primaryCategory': "lifestyle"})
                if article.get('primaryCategory') == "lifeandstyle":
                    article.update({'primaryCategory': "lifestyle"})
                # politics
                if article.get('primaryCategory') == "Politics":
                    article.update({'primaryCategory': "politics"})
                if article.get('primaryCategory') == "UK Politics":
                    article.update({'primaryCategory': "politics"})
                # science
                if article.get('primaryCategory') == "Science":
                    article.update({'primaryCategory': "science"})
                # sport
                if article.get('primaryCategory') == "Sport":
                    article.update({'primaryCategory': "sport"})
                # technology
                if article.get('primaryCategory') == "Technology":
                    article.update({'primaryCategory': "technology"})
                if article.get('primaryCategory') == "Tech":
                    article.update({'primaryCategory': "technology"})
                # travel
                if article.get('primaryCategory') == "Travel":
                    article.update({'primaryCategory': "travel"})
                # uk_news
                if article.get('primaryCategory') == "UK":
                    article.update({'primaryCategory': "uk_news"})
                if article.get('primaryCategory') == "uk":
                    article.update({'primaryCategory': "uk_news"})
                if article.get('primaryCategory') == "uk-news":
                    article.update({'primaryCategory': "uk_news"})
                # world
                if article.get('primaryCategory') == "World":
                    article.update({'primaryCategory': "world"})
                all_articles.append(article)
    return all_articles


def get_articles():
    data = get_data()
    articles = []
    # filtering out unwanted topics
    for d in data:
        if len(d.get('body')) < minLength:
            data.remove(d)
    for d in data:
        if d.get('primaryCategory') == "environment":
            articles.append(d)
    # filtering out short texts
    print(articles)
    return articles


get_articles()
