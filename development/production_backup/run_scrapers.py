# Import custom scrapers
import bbc_informfully
import independent_informfully
import inews_informfully
import sky_informfully

topicList = ["business",
             "crime",
             "entertainment&arts",
             "football",
             "health",
             "lifeandstyle",
             "politics",
             "science",
             "sport",
             "technology",
             "uk news",
             "world news"]

# Flag articles
def flag():
    newsFromToday = []  # Collection of Article-obejcts

    # Any article where the topic is != environment is marked a filler
    newsFiller = []
    newsGarbage = []
    for item in newsFromToday:
        if  item.topic in topicList:
            item.flag = "fillerArticle"
            newsFiller.append(item)
        # Any topic we do not want to recommend any further (e.g., environmental, travel etc.) gets discarded
        else:
            item.flag = "garbageCollect"
            newsGarbage.append(item)

# Scrape
def main():

    # Run scrapers
    bbc_collection = bbc_informfully.scrape()
    independent_collection = independent_informfully.scrape()
    inews_collection = inews_informfully.scrape()
    sky_collection = sky_informfully.scrape()

    # Flag articles
    flag()