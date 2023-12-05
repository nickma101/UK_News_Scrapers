# Recommender and Scraper - UK Experiment (Week 1)
import json
import os
import random
from bson.objectid import ObjectId
from datetime import datetime
from bson import json_util

# Custom scrapers
import bbc_informfully as bbc
import guardian_informfully as guardian
import independent_informfully as independent
import inews_informfully as inews
import sky_informfully as sky
import standard_informfully as standard

# Script parameters
DATE = datetime.utcnow()
TOTAL_ARTICLES = 26
ARTICLE_PER_CATEGORY = 2
ALGORITHM = "UK-WEEK-1"
TOP_POSITION = 100
POSITION_1 = 1
POSITION_2 = 5
FILE_NAME_NEWS = "news_articles_"
FILE_NAME_LISTS = "recommendation_lists_"
WEEK = 1

# IDs of manually curated articles
ENV_OG = "655b82bf444d43b4b27e8856"
ENV_RW = "655b831c51ac331ac1a5295c"
POPULAR = "655b885651ac331bc8b9548c"

# List of article IDs for each category
BUSINESS = []
CRIME = []
ENTERTAINMENT = []
FOOTBALL = []
HEALTH = []
LIFESTYLE = []
POLITICS = []
SCIENCE = []
SPORT = []
TECHNOLOGY = []
UK = []
WORLD = []
FILLER = []

# List of user IDs for each group for week 1
# WEEK1_GROUP1 = []
# WEEK1_GROUP2 = []
# WEEK1_GROUP3 = []
# WEEK1_GROUP4 = []

WEEK1_GROUP1 = ["cnXxeLqsavZkPdyMY","F9ydu9B87AWbo2nFy","KGrN2PbK3vSB53Bwi","2bx37xNAEwFZMTEiD","y8KgpaqXd22kg9G2x","KyvhF2KQ64MYRphX4","6jPSkFpoJXrCBXuC7","6eTZ3JY5QbaQKsykT","TX4jrx4GRvjsKxTEt","qWGu2kpNFmmc7R7bG","cnXxeLqsavZkPdyMY","H4q94wjmTmcxMocdX","JxAdW9un6qRmeZLns","Ntd3nwcXsZva4FhWR","mx7Lx2mdtiwnMQAKr","D28PbrjDFv76EtDaD","xkYa6PFwS5DfqFDHy","QDx35vgRQtFsbPcXW","haCm3h5Ag9TyjWXyc","zFirubuDK6F98Fkre","KGrN2PbK3vSB53Bwi","KGkvkooBrygF2vdDx","JRZejhwwJqsZcdhrK","DC7eHC2SPQ4s32xba","HLRDdJoD9t6JmypQd","SpYFTzCy2xFuQhCPM","xkYa6PFwS5DfqFDHy","Nqpp9dXxGwP8A45P3","TLZikSGdyRETkG37g","Bd6qGsZ4nCSyfvbFJ","fYkfCF65kMLndXMMQ","PTbmK9dqKABBJGiDT","RDL8adSLeFrNbw33Z","nWv5AkxyWS9wJwhiX","Ntd3nwcXsZva4FhWR","C26LxqSDWbNpkwHvc","pBhx8pSFQoFfrsZBD","3vy6EJjgGyqX8RQog","cEAEQqhFqbS5dz3GH","bXd78amaJTjqbo9Tq","LWaNPbFcKRiXd9cYA","5bNipF3Fqna95gqRW","J2wBatJskicjoJsMq","PTbmK9dqKABBJGiDT","QjSTxSX8EKBNDyeXr","7gnqvmaf6eDx4Kv4H","HLRDdJoD9t6JmypQd","Ntd3nwcXsZva4FhWR","oyLhtBaeRSrPkd64Q","MnSRX95LoLNtMcEpz","SpYFTzCy2xFuQhCPM","WRmC6DzMJQ7vz5YGn","KGrN2PbK3vSB53Bwi","xoSLpgjP6fX9zEkWJ","ZEKvGpCHTNzpeFGcC","rziYHfGjbKes9qggw","Bd6qGsZ4nCSyfvbFJ","utZpCHGFJkbfy4PhQ","bXd78amaJTjqbo9Tq","zSbmKZsZM8qxSx2sj","QRERdrPxdyvG3SHMC","cnXxeLqsavZkPdyMY","RemDpFpsSYizGbjuh","uZMTwcTPw5SJoratm","KGkvkooBrygF2vdDx","yLW5fRgNTzNmStgLF","YqZSmcFNvN8JTzao9","KGrN2PbK3vSB53Bwi","44LegAqixZv4EwEvX","QfNDR5x4vvD3kYAZq","mx7Lx2mdtiwnMQAKr","LWaNPbFcKRiXd9cYA","jv6yGXM59xkaJnZbi","CPAeEgYk5Dt6hmtfH","eaTwBSF3ymSdKE9Lb","PLwxnuKjMjvDtak8W","6eTZ3JY5QbaQKsykT","Sqvhe6C5FTXnNxpQf","5sciKhiS6ckvsJqCx","h7CQBnQzxZEgZXdNX","uZMTwcTPw5SJoratm","wE8sMPtxjPKoqif3j","WdHj9JFwzywanvSmP","pBhx8pSFQoFfrsZBD","KyvhF2KQ64MYRphX4","9ideSK8xuAzY8jFCx","3MFdLBb2ArQCTwYn4","FGyT5LEmoCyWifF8e","YqZSmcFNvN8JTzao9","SANDWzPgrPrTeeArH","WdHj9JFwzywanvSmP","qCspq8W5rWQprwveX","5PPA2YL3B5iqQ9S65","hoCZd3uYvGhFzLMAY","RLBFcqGujwHQYkE6i","wJ2cDdL5GiuDhe8dd","CyG4f6EH58byo9CDg","KYmYAmfbn4p65L4sL","HLRDdJoD9t6JmypQd","5KGm3v6TQCHnNeY37","pn73o2chg9ZaCAP6y","fYkfCF65kMLndXMMQ","AeRAWfsBqL4tYK8eu","eyHacBmt4DakAhfNh","3MFdLBb2ArQCTwYn4","sC6Wz3NoWEcwbXjzR","sYikBkbzYb4oyuWm6","rziYHfGjbKes9qggw","xnPev7pmZREc42AXZ","C26LxqSDWbNpkwHvc","nitQxp6KCu5omFXKL","ziaAx72KGLo2jt3Am","JujeCWZLpCm2i3Sdo","oYb8hGmPBJ2ufHTKs","Sqvhe6C5FTXnNxpQf","7gnqvmaf6eDx4Kv4H","barfYKbjrvJaQCBuh","vaBA2mtKWtmqSpa3n","QfNDR5x4vvD3kYAZq","6qukXfCki9uGx8iJ4","LWaNPbFcKRiXd9cYA","CPAeEgYk5Dt6hmtfH","ngS55MJdx4Qne5oHA","owY9ThTcQ7aQ6nBMQ","BhWjC7SGCPkmwKbfJ","cprWCdqz9okjeWyv4","o96wrCFQop6PWCQvY","vaBA2mtKWtmqSpa3n","EwYkE6QkvDG3fF6Bn","dw3yFss3apXNYsPcK","Q8fgS5pzbNagAG6NC","TLZikSGdyRETkG37g","utZpCHGFJkbfy4PhQ","hoCZd3uYvGhFzLMAY","idsWYuQboRdpvAnB3","JRZejhwwJqsZcdhrK","haCm3h5Ag9TyjWXyc","CyG4f6EH58byo9CDg","nZs4YueE6NA9DLhSs","K4SRf5CJhpE6RCPW6","2mscLyCGFWAk3Atp8","4zwfSBi45hfEKPo8c","Bd6qGsZ4nCSyfvbFJ","KyvhF2KQ64MYRphX4","rdyGbZ6ByoxNYL6FZ","4xApn9fiNmzp9XtHS","9oSHQBHzBkNBPkfE7","qM8uBz3RbkavPd5c4","hoCZd3uYvGhFzLMAY","ukdbY4cPE98cRTgFD","sbrRqPzYP5pcPTaKB","KNEmGjtBSHM7daBmd","D28PbrjDFv76EtDaD","cEAEQqhFqbS5dz3GH","2bx37xNAEwFZMTEiD","5PPA2YL3B5iqQ9S65","PzfKn3LqCcp7bL4za","3vy6EJjgGyqX8RQog","DC7eHC2SPQ4s32xba","woDe2G4bRZkr5ofso","nWv5AkxyWS9wJwhiX","zSbmKZsZM8qxSx2sj","haCm3h5Ag9TyjWXyc","ASx5cQ4io9PpRv924","D28PbrjDFv76EtDaD","o96wrCFQop6PWCQvY","bcdnamsysdterrBLx","jo5nokCBP4XkJNKmd","mW6SsqEPXK3xKu9gQ","cEAEQqhFqbS5dz3GH","6eTZ3JY5QbaQKsykT","xeG7yqpDtzxc8Pxim","6eTZ3JY5QbaQKsykT","HFFRYweymwCWoJKM6","rdyGbZ6ByoxNYL6FZ","wE8sMPtxjPKoqif3j","6qukXfCki9uGx8iJ4","mx7Lx2mdtiwnMQAKr","X8uFk4sLoH97wnTRK","ykm52FPoioEaqMjRk","5CoCvbqgJjZPqGbp2","mx7Lx2mdtiwnMQAKr","CyonycehAQTgKc2ot","bCgFDjjwhh3kNPDLh","cnXxeLqsavZkPdyMY","haCm3h5Ag9TyjWXyc","Zc68v6dh8tQShDEKh","dKTd4nwSjpQZDuKKn","DRCdYEK8HheCju6Lg","4xApn9fiNmzp9XtHS","Bd6qGsZ4nCSyfvbFJ","KGrN2PbK3vSB53Bwi","Bd6qGsZ4nCSyfvbFJ","KfsJ8QLXcCaqq43bd","eaTwBSF3ymSdKE9Lb","PLwxnuKjMjvDtak8W","sp9jRzn3aoATRGrve","x6G8wi4iNudTTNXhG","X8uFk4sLoH97wnTRK","KGkvkooBrygF2vdDx"]
WEEK1_GROUP2 = ["vyxBFXfSKzccTpMh7","nQvNpPtwzKBrNPLJm","JC48QSh53PTWgWFww","FB2uYpv2R66r5oLsq","6nGrHJevHtmqH5GPd","4w6wAjJeqNwGZM3hm","jeSXKRZyQMib3gHFC","etAAzoJEzESpLryMF","eQhhJuXzJ9u2h2SAN","3dtnQbRD6E8a9C894","yuYonjebaBaFDhxPN","Bcd3Z4emWgRHyb2SM","35ZrSsPQPJkEHZsk4","4TG7qit8dGucvkN8P","MsvHiinu6u58ZjKrw","sHT7ND3sudoqmhwow","myBwoskFCZ8RG7KxA","WZjfhERFC2KjAt6Mi","ZtBGMXQdrEFASm2Jq","sHT7ND3sudoqmhwow","2rGCsWHB2NtmjkNrx","h5RfRiHTzw6cKzQZB","2CQb8JBQkJiZ7EZjR","jeSXKRZyQMib3gHFC","etAAzoJEzESpLryMF","R7AWwsaJ48GD9h8Qx","Xm8gnZiyeW4jiWkKx","szgEN3zLxKH9WTDoD","2j4553MvSCpcKbnFo","wEaTiLRRkPHwY3k5w","6eRSusFjhNdQTkkiW","vwd37tSHAsveiSCd7","ev5ALqN6cSKwHfKmK","4dgXQ3MLYHtpepBbF","2j4553MvSCpcKbnFo","pyzoEm5CAmcqucaeB","MHu9tdXNP2GhZrwgD","efXtRu34APvB9bk4C","HrohG6D43cKyRHZdH","xjtNfM49LMzEg34RZ","DGFmieiLD7FErs3eA","XXqz9MDbmfWnNFvF8","jHdmoBGz5DdoCheZS","JA8gbwy2TqDh6CtHD","pyzoEm5CAmcqucaeB","pQ7KgB7eHWxBupomY","rGECFbHZQJarumBTT","YnMFvgbnmzswvksqa","WAamSFCaMFNmAaXx9","XzwnNtTiMkp4Ltcn7","udytDFdCxZoSmzM6e","v8x7soDTiN6Hcepyn","tjxYTGxMSWGJQo3JN","5GzjHckDkvraQzLw4","rnqff2Mt2TSrp8PYT","uQCFuZ8sKFkSzMhxp","C3ycYPDwCskXwhQhe","vR5ACrKYdrFGxArdM","wuM7pYX7YqM6YC3k2","q3YS5i2HT3SuS8HtZ","wEaTiLRRkPHwY3k5w","Qp4kGunPoKvWcnjRd","BiWvvAMQKZLYi2kej","4bPpte4GmjDgzt3dE","fDDpRpCgnHdjoEt9q","sAjyrDYcnYyDpPAZB","FB2uYpv2R66r5oLsq","R2jdnSs5EhDuvhBQc","tQRgSshAJmoHcEHvL","xjtNfM49LMzEg34RZ","XY4pL3wrCbaEb6kdy","nQvNpPtwzKBrNPLJm","asAqRacATaeXBKh6E","35ZrSsPQPJkEHZsk4","KsPAh7zYp6AxBHZjp","t4xCziWCScphgGSz4","QE45jdwpXg2b2nB8j","frtYNZodDMncbZYzm","fPHF9THi8ahKgWRkN","GQo9L6pbSCuAx5Cwg","9CZc9G9qZGJsjk2ay","BsSWxA8ucCsv5z7fL","udytDFdCxZoSmzM6e","DkK7kGapkCXEttnxM","XXqz9MDbmfWnNFvF8","i7qtzx3e4MfJjC6bQ","jfHdotZSCrygamyAv","4w6wAjJeqNwGZM3hm","2rGCsWHB2NtmjkNrx","GQo9L6pbSCuAx5Cwg","LQGt7MN6tC72SLjLZ","3dtnQbRD6E8a9C894","i7qtzx3e4MfJjC6bQ","rnqff2Mt2TSrp8PYT","WAamSFCaMFNmAaXx9","BiWvvAMQKZLYi2kej","7dKF9pypJTT9QfYQ6","SLywkzFAzsPDwNZsw","jwSQWWTmawmEZQtzY","QE45jdwpXg2b2nB8j","6nGrHJevHtmqH5GPd","pGaobDKSWjJbTiMez","c7QZ4KT7z97XSB9Ct","uD6x2jHpYJePqXoDZ","GbRgQp8XENTvxAAwa","itLjvWYRw9XFw6x4F","q3YS5i2HT3SuS8HtZ","fPHF9THi8ahKgWRkN","yeYr96fKsKndmrte7","uQCFuZ8sKFkSzMhxp","4w6wAjJeqNwGZM3hm","wuM7pYX7YqM6YC3k2","tQRgSshAJmoHcEHvL","q3YS5i2HT3SuS8HtZ","XXqz9MDbmfWnNFvF8","tjxYTGxMSWGJQo3JN","GbRgQp8XENTvxAAwa","5GzjHckDkvraQzLw4","86ermATgASzwEM3xd","X6FayGCyzfW2eqsaH","ujNCjuDW6YqHrSxJF","BFD75Ku3q7vDemext","xjtNfM49LMzEg34RZ","ftCBxenT5n8Yym9tK","JC48QSh53PTWgWFww","gQ4vn8cuQHvMwxDhZ","fPHF9THi8ahKgWRkN","vyxBFXfSKzccTpMh7","6j6E3G697CYqhYzLa","JC48QSh53PTWgWFww","QibRJjjLkM9rwvoxx","8YSYSkEnnEMb3knev","nDyy8Rcc9ETnkhqCD","EZKEBdytgt2dmE9y9","efXtRu34APvB9bk4C","sHT7ND3sudoqmhwow","4dgXQ3MLYHtpepBbF","GQo9L6pbSCuAx5Cwg","Xm8gnZiyeW4jiWkKx","ZXhbMu9m4AwKrg8Yq","YvheLdotHgB39gJHu","8YSYSkEnnEMb3knev","9CZc9G9qZGJsjk2ay","5of4ooQsCgxLCqr74","h5RfRiHTzw6cKzQZB","ECzk7jcJ9Y4Bxm8RE","uQCFuZ8sKFkSzMhxp","HfENXDhLpxAWcdGPp","XY4pL3wrCbaEb6kdy","fJRCRzXsXExPg4T9v","aEeYeJ8hqKiCjB83q","vtRTwG7iPATSRknY5","86ermATgASzwEM3xd","MHu9tdXNP2GhZrwgD","nQvNpPtwzKBrNPLJm","aFLjuZLKSdwCAhZ8q","SHRwzqAuWNNaYwgXS","vyxBFXfSKzccTpMh7","etAAzoJEzESpLryMF","8JRPbA9rRRoevNiRK","q3YS5i2HT3SuS8HtZ","MFQE4JXRWdv5vpBDX","YnMFvgbnmzswvksqa","B7M4qcy68ZTwLyvED","vyxBFXfSKzccTpMh7","i7qtzx3e4MfJjC6bQ","SLywkzFAzsPDwNZsw","86ermATgASzwEM3xd","C7JGQMHCpteDzA2xE","vwd37tSHAsveiSCd7","SFkz6DMyr6PAoBwtu","xjtNfM49LMzEg34RZ","3dtnQbRD6E8a9C894","wEaTiLRRkPHwY3k5w","miyyvwm8aBbHN46wZ","8QxQdWBbaiJMQuzoo","CAX2KxpgsDh5Faet8","4TG7qit8dGucvkN8P","q3YS5i2HT3SuS8HtZ","gnq477fxzs3zDnXNB","hZqoAcjXQE7d7AN3S","rnqff2Mt2TSrp8PYT","vR5ACrKYdrFGxArdM","uD6x2jHpYJePqXoDZ","8YSYSkEnnEMb3knev","ZtBGMXQdrEFASm2Jq","uD6x2jHpYJePqXoDZ","Xm8gnZiyeW4jiWkKx","eQhhJuXzJ9u2h2SAN","PkGpwiiPJrQwmPMiA","gQ4vn8cuQHvMwxDhZ","RoXpNvDLiuQBjZ7hr","yeYr96fKsKndmrte7","R7AWwsaJ48GD9h8Qx","jHdmoBGz5DdoCheZS","ugTgCkq5Bjswib3x2","gQ4vn8cuQHvMwxDhZ","4bPpte4GmjDgzt3dE","jwSQWWTmawmEZQtzY","gQ4vn8cuQHvMwxDhZ"]
WEEK1_GROUP3 = ["t3GbPvBaGpGKG7aWp","uau7qfb97NTGbffkC","XNwXo8BYwmJzAbeaD","bjpHCfpSd8zyTomXX","uau7qfb97NTGbffkC","yo7pfq2gNSyKCajJi","7FCWfHmRZMH6zifdM","SprDFnZ9WR5d42BBG","oEAxKZZeyq24PQzMM","y7Qs8NDCHsE8oi53A","ZYASew4hj2gNycGi6","ZcmphZ9SpJicFXKLf","86YQ6MMgh8pLdPHv4","WX7KtMfKxRLQjbCpf","KAS2cv5xZd8vXCyCf","WLpfLj9JBfDbSX7cq","uiprLwX26GbAZys8a","GkeZa9AWBv7GKeN3d","5xcWML4Ybd6vPep9J","w4r7x5xYqBTE4W3qR","xqpgEroC8koCPSbk4","Yxhmif3i3ekeq3G7P","9bHhqEzAHaZzqvjcm","q65Jjd4CZgAF86ZSo","vrGy7fzJtxoEguvEh","JgYdSZYYGrH4eE3HC","J47R245LaWdoEmQpr","TTQ8kKSFEXaFDfZYp","GkeZa9AWBv7GKeN3d","CwunfXCNdnsuc8o2m","cdqZjdiRe3DMQN2G8","BKCZjHEGxmL7oFJwK","iqPWkrQw6tS7LQ3ph","eE8hykLCKcxu5ajn4","CWzfQcHEvDhkhz2yJ","CWv9thDSSmMsmBKiG","rC6vXDD9kJvp8MTf5","HaxwJsXtou92c8yM4","R2b68REQSfcPYYuWD","kzhYtERWnfHRdQrYF","MsuLpH3oKD2eougDs","coXJFRBqykMzi4AZn","Ag4pnn5Qj3uzQspeW","ihAes6J6EHrXEEhNs","z7zHe78uyknQrodXD","S5SiezfnEe5tznXcW","KSQGte6pFTdoHfpMK","QyoZ6p3nXpPX6nbvi","coXJFRBqykMzi4AZn","MqiA56xNfQ9iyRgCw","FAv6NtPS7pznXhW5v","4nCqjsvRHbskQGyRa","nkqShxK6kp74bBiy6","pN4o7Kr5fJuGhvw7u","CWzfQcHEvDhkhz2yJ","t6x7qQgLvgza7frkL","XJKZ7L7oQoppWMyw3","xtXjNjYrxACmeWyMx","XJKZ7L7oQoppWMyw3","P6FuNcoEMFgp2awGT","Ls5apdeMawNSdmaDs","XZZFK4qyZ8j4jCDiD","z7zHe78uyknQrodXD","KRHKvogbe9LfKGmYS","76ZCRvGPMtCAxv98G","FzR4jGEbhS5hJuKNJ","KRHKvogbe9LfKGmYS","2NJmodtSMNRvE2NiE","uErXgBw7Rc7DKNdXn","oEMgkhgMm7kqasq7C","PDKh5hm5kiZ6pd67D","G6PAXoiehpeRqM2Ti","Fkj38G45zad6M2YNz","FgxpNrDA9hdz2iK3q","76eFE6GwTXKXPKiGw","zeuSt5Sdipn5rTFWw","eJMdx9iKqDEmoMeKT","uBKE6eDWQys796iwr","kiFQgAygsWc9Byh77","7FCWfHmRZMH6zifdM","hbhT5HRpK6bkSkPNp","q3HNDousdtAHseKG9","XRiZF4F2sdztwWSFG","CWzfQcHEvDhkhz2yJ","xM366Tjso72AtA2NX","fx7QydSfcEL7gzESv","kShR5GvDwQhLfa33i","8u9a3A8fA3HGAbtmo","FgxpNrDA9hdz2iK3q","2a2ndtLuxv8dqDm9E","KD9MF2Y8QzduLznwp","woDr68BDJPSX7Qvgt","ZaEbyWwJbvy3ss5iA","86YQ6MMgh8pLdPHv4","bRpf3tmkPgw2J5xvM","zuvYqoZ7x5rSyTSSK","9n7NZ8B8ZGwJt9eAd","Fkj38G45zad6M2YNz","iM2sR8ubazv9XFpN9","q65Jjd4CZgAF86ZSo","tKp77ugmTDBJ4uzCL","TRCej8sRCAQfHuEXP","G5ExdsigsZERWi7wD","FgxpNrDA9hdz2iK3q","pRn9XdtnGZMtCuN7e","y7Qs8NDCHsE8oi53A","GkeZa9AWBv7GKeN3d","yDdvyuxg7AnKHxj3h","2NJmodtSMNRvE2NiE","tWQJ6dzZDwYwuYLip","fCSD9Ct5HK8DR3LcN","eqr37oQEpKjnLCrSC","tBp6Gs5GLcLooAXXQ","GTvfzmTGcLk97XPkk","iqPWkrQw6tS7LQ3ph","kShR5GvDwQhLfa33i","hXLGFtETT22SjLzoE","Yxhmif3i3ekeq3G7P","XRiZF4F2sdztwWSFG","XRiZF4F2sdztwWSFG","ti9C2PCczxE8dLyMe","h3t36WzFTEopRTfAq","hRQimY8vCrqP5AbP5","7AnzA4HqrEctuvLQm","xtXjNjYrxACmeWyMx","TcRYhRx3J2xMbJjk2","xqpgEroC8koCPSbk4","ApS8YWr3rLN8pGGnR","KPshNQc35A2fdi2oh","fCSD9Ct5HK8DR3LcN","MqiA56xNfQ9iyRgCw","J47R245LaWdoEmQpr","gfGcfcWW4Gj8bmayr","KD9MF2Y8QzduLznwp","KMhRzoqXSxyNsMKJu","tBp6Gs5GLcLooAXXQ","ti9C2PCczxE8dLyMe","GTvfzmTGcLk97XPkk","G5ExdsigsZERWi7wD","aegnfDvjate2L5GRC","ZeFS9oYhmYvb7kSSe","LDgEZfnHAc7MyQa8c","8xiZikhK9hg2qQetX","TBfnotCAztryfZnfu","w4r7x5xYqBTE4W3qR","CATcXiRvEuEMMyq4n","Q36Y3r5jX5JAutiyS","JgYdSZYYGrH4eE3HC","uiprLwX26GbAZys8a","cySPF7ZJQrvm4gLZS","7AnzA4HqrEctuvLQm","9JtXdTo8dYDa77tuG","iHZ2Y5ZeMZZ2RfiuT","s7SNGu2a72dbTMTnq","Q36Y3r5jX5JAutiyS","9JtXdTo8dYDa77tuG","FzR4jGEbhS5hJuKNJ","CfiKa3vC88z7xPpBy","tWQJ6dzZDwYwuYLip","HmLmaYCBRCN4gNphn","vi6ZXNnLXhKR9kKDF","2QaNpZLeRdnLJXQGM","JLtrz7ndhQgHXnfPY","aegnfDvjate2L5GRC","ZnZBEwxSXFEkY6kzM","gfGcfcWW4Gj8bmayr","WX7KtMfKxRLQjbCpf","t6x7qQgLvgza7frkL","KkvyFBhxdArjJy9BE","tsTDYFq5TkmsiwTZu","2a2ndtLuxv8dqDm9E","q3HNDousdtAHseKG9","xM366Tjso72AtA2NX","5xcWML4Ybd6vPep9J","B25eR9uxq5Ca98pqm","oKy7NoRKWyyKmmiX8","G6PAXoiehpeRqM2Ti","XNwXo8BYwmJzAbeaD","FzR4jGEbhS5hJuKNJ","uau7qfb97NTGbffkC","m3kCMwWF4Kc5Q698t","woDr68BDJPSX7Qvgt","yDdvyuxg7AnKHxj3h","TBfnotCAztryfZnfu","NZJJs4xy4nhsLnEgc","FAv6NtPS7pznXhW5v","qzEiBMuhcFgLx8G6h","PDKh5hm5kiZ6pd67D","eJMdx9iKqDEmoMeKT","qzEiBMuhcFgLx8G6h","8u9a3A8fA3HGAbtmo","5w4MxkMmTQMrh3SSA","pPyipFEGhsmp4WQaD","s7SNGu2a72dbTMTnq","oMR8sZoQuGnEGWM83","phJ8aoZ4QR8bwotdJ","TzymM7TyYWmtjcyFA","xvxXPdvSRKzuKwMRQ","q3HNDousdtAHseKG9","G6PAXoiehpeRqM2Ti"]
WEEK1_GROUP4 = ["jEJQBuYpFLyYfiW3B","HvwATups2zysWTqmQ","FubcpZtfQ8onozo4L","AhasZvMm8i8quFT8s","jAmyhkBcf36Ry34tJ","S7tECgEqpi7c5fmxQ","aLxc8NBd77fSBaFQi","7yjvQfS3FfkyKaio2","ivgyfvjWAT5Ajwtzt","z6xKMngK7jXChtH4D","u5hdyfqYbxBtWqzQt","fKM2h7NwTkN2TJrqv","P5tNedcF5SkrYjqAc","xRzXhF6uE9fntfyfo","pTGJPeGAjJCHzvghx","azm3enyrTSyqJhj8S","NG5BFKzkmaiG87fup","degB3AQ9yuxtedQE6","gfSKhN4BaSMXi8Cgr","MrAMSew6QXJ6DHnkY","YebzCNwRwwv77c3H7","25Y9bZSwP6mo9cArc","P8oKScYGN5EMWtTi8","KkcSYuYaTFBiwn4Qe","vZADMXMMjnMEQtxcR","KzxQtuFeWmsx2JPgy","CTFNdLaQFhBTsWf9o","nF3fo4eGH5DbAatcM","rBHLrnMcJm8Zr4h6K","S7tECgEqpi7c5fmxQ","RJL7zihFChE4Qtz9C","HYKRiXAh4A87Y4AXw","efpGxECiypQ4fSHrK","j6ng6YKCN3v69iE5R","Q53oiKYyRFT9DJiud","HFTyLQdoLQCqY29yq","cCsMgmaGgN5HyBtoM","WRjnjZFaXkXAcguT8","keCp4jk6qN5RerzNc","xRzXhF6uE9fntfyfo","3y2w22aFsNGRiCr7w","XhS76XZog2hSCQEGr","yEGe8BtFFB7xXCviC","pTGJPeGAjJCHzvghx","HiKMBFi79MW8Wkowe","BL5gRcN3JHWWJk3G3","W69zJTpdj2pWNZr8z","vWESbacfmNv32Fcbq","i295gbHHW9tWiLy7y","7yjvQfS3FfkyKaio2","tCaPfSSFqCvPRBYWA","7qSyRBzubM5ppyjCK","XqxToSFTYoDXsn2jr","Y5XfDW5dDeGh6mmfR","JRPFZ9aYjs8wvCLB4","buwpARj4P7veZ8rfM","3y2w22aFsNGRiCr7w","QtYZ78z9t7uRKGvRT","oe4YriD29bqvaMzPh","ThJ7Qct46rEpHKamP","JHEgYCAAhH8QWpCMS","ttErqLNi4yR9vzKQt","W69zJTpdj2pWNZr8z","2vSbi8uoJfvXm2Gqs","9Womx7t8Z9q8TYFsw","ZNE6MtF2kJjQ4k5Ls","SDyEbyPt85yH9HsGs","tCaPfSSFqCvPRBYWA","XnZbjyKKSnLgKFN35","JRPFZ9aYjs8wvCLB4","j6ng6YKCN3v69iE5R","nF3fo4eGH5DbAatcM","wTFNC5KxmsqmrDQqf","gkDqqfqeeq64aoWLH","bpBm8rgwrQdfdkkw5","kEhHwZPN54rZ5So7o","degB3AQ9yuxtedQE6","kEhHwZPN54rZ5So7o","sL9DCtS45usBcLsDe","yEGe8BtFFB7xXCviC","5t8xkHvAKJWZAD2P9","JHEgYCAAhH8QWpCMS","Ar4xhu8ZCtFPAXnKM","FubcpZtfQ8onozo4L","7yjvQfS3FfkyKaio2","a6u68iTEXXXDTmzvg","zvCrMJCHCSCnDiKb2","cowYHFS29WpsGpDRh","7dKJ5tRzMQQS8WPDQ","uuZNquPckGn2QHGxW","7dKJ5tRzMQQS8WPDQ","JkSXeZDW58Cwjatwc","xRzXhF6uE9fntfyfo","vtZMvrCugjFjwcoCP","xRzXhF6uE9fntfyfo","QN8Lus36dzbzqZmuC","wfCeqpwmrnQfb56iS","F6No9SYGczexmrt5R","azm3enyrTSyqJhj8S","GhBxhhvyDNYzAbYcS","HCRAQriqt3QKmhYgQ","vsQrJBQRuaKcrqdr8","JQYDRRrXJj4xGmyRo","cCsMgmaGgN5HyBtoM","PuNjR8dyqbmzJvgWZ","HCRAQriqt3QKmhYgQ","sTfd5k3hCm4dbpB24","bpBm8rgwrQdfdkkw5","3SzvJyujtBTWtZpNm","JHEgYCAAhH8QWpCMS","HFTyLQdoLQCqY29yq","fKM2h7NwTkN2TJrqv","ZNE6MtF2kJjQ4k5Ls","y4qzC3vYkDc4tTmfj","HNbfQJnQC25hbXWGz","vtZMvrCugjFjwcoCP","PAFFEAMMWjxuE55c7","xwQ8miQrqvodTb6y8","ZNE6MtF2kJjQ4k5Ls","Q53oiKYyRFT9DJiud","eptXbzWMusBm2Thb8","JgDbDnTbeLXe2HRww","cXy4KkaockjEELvyJ","AhasZvMm8i8quFT8s","PuNjR8dyqbmzJvgWZ","buwpARj4P7veZ8rfM","yEGe8BtFFB7xXCviC","wNmSeMqTL8Q4ZLf7S","buwpARj4P7veZ8rfM","HYKRiXAh4A87Y4AXw","vZADMXMMjnMEQtxcR","buwpARj4P7veZ8rfM","nF3fo4eGH5DbAatcM","j5CRu6huFzvQjTiXp","JgDbDnTbeLXe2HRww","Qdv5jqNkYTMN4P6df","zn5gAnX2uahKxgLeC","qSokBL6qjz3FN3ZeY","ivgyfvjWAT5Ajwtzt","pxeT4Wg9ApJfWGi7K","6pTHfwEcuX2kuBLWN","2XnZcP4XnPFQyomyQ","xwQ8miQrqvodTb6y8","rBHLrnMcJm8Zr4h6K","6bi45YbZFe3vaztwn","5t8xkHvAKJWZAD2P9","YWnnzdfKG6byh5tBB","95K29ryshm2Q8G5W8","XvvpyzFY5DxihSshg","PAFFEAMMWjxuE55c7","9Rp3RvzK95GAJF62L","pRnt6KHA9kgQS26o9","PAFFEAMMWjxuE55c7","MwRdGeEEiQ23nZXLq","S7tECgEqpi7c5fmxQ","9Rp3RvzK95GAJF62L","JHEgYCAAhH8QWpCMS","zn5gAnX2uahKxgLeC","aLxc8NBd77fSBaFQi","JHEgYCAAhH8QWpCMS","YnEHWhBLddkQF7y5b","bpBm8rgwrQdfdkkw5","PuNjR8dyqbmzJvgWZ","F6No9SYGczexmrt5R","JEBFHQFphirBAhNAD","7dKJ5tRzMQQS8WPDQ","2CffThPzuAZCTXWfN","sL9DCtS45usBcLsDe","23g7LwZEmKdFLMM4k","NHWD7jmQuKSwiBu72","FHCwJ5J8rgjJAjiwz","EAo2ESrn55WoeJiiz","6pTHfwEcuX2kuBLWN","Qdv5jqNkYTMN4P6df","kTidAsbgbiZWyMB6A","7yy9yuLTaZvRPv4r2","wuxG2pGpQt3FJi3HP","NHWD7jmQuKSwiBu72","MwRdGeEEiQ23nZXLq","buwpARj4P7veZ8rfM","RJL7zihFChE4Qtz9C","r8jtjJWHR4oudDtx7","xXxwzfucowQHZqYZm","KjrNZ8Sb83AC5ox8B","szE3sRKQ3E4Fge33z","ELvC86ProynPQYzNe","xRzXhF6uE9fntfyfo","gqN2AJ9igQ4is3r5n","wTFNC5KxmsqmrDQqf","i295gbHHW9tWiLy7y","BL5gRcN3JHWWJk3G3","NG5BFKzkmaiG87fup","YebzCNwRwwv77c3H7","P8oKScYGN5EMWtTi8","pRnt6KHA9kgQS26o9","ttErqLNi4yR9vzKQt","EAo2ESrn55WoeJiiz","wNmSeMqTL8Q4ZLf7S","HNbfQJnQC25hbXWGz","wzTmEib3xMkLfnQ4y"]

WEEK1 = []

# List of user IDs for each group for week 2
WEEK2_UNCHANGED_GROUP1 = []
WEEK2_UNCHANGED_GROUP2 = []
WEEK2_UNCHANGED_GROUP3 = []
WEEK2_UNCHANGED_GROUP4 = []

WEEK2_IMPLICIT_GROUP1 = []
WEEK2_IMPLICIT_GROUP2 = []
WEEK2_IMPLICIT_GROUP3 = []
WEEK2_IMPLICIT_GROUP4 = []

WEEK2_EXPLICIT_GROUP1 = []
WEEK2_EXPLICIT_GROUP2 = []
WEEK2_EXPLICIT_GROUP3 = []
WEEK2_EXPLICIT_GROUP4 = []

WEEK2 = []

# User setup for week 1
def setup_week_1():

    # Adding test users
    WEEK1_GROUP1.append("vE3daNTcMj82yJ4g3")    # User: 383RT, Pass: 3DQra
    WEEK1_GROUP2.append("EhAcgf8zq9EuFKzno")    # User: 499zX, Pass: ChF6e
    WEEK1_GROUP3.append("9tTYSuL75rxtevWus")    # User: cdiky, Pass: sak9m
    WEEK1_GROUP4.append("bMyY9MiyvyYuDLovJ")    # User: i5w7k, Pass: igX5Q

    WEEK1.append(WEEK1_GROUP1)
    WEEK1.append(WEEK1_GROUP2)
    WEEK1.append(WEEK1_GROUP3)
    WEEK1.append(WEEK1_GROUP4)

    return 1

# TODO Writing
# User setup for week 2
def setup_week_2():

    # Adding test users
    WEEK2_UNCHANGED_GROUP1.append("vE3daNTcMj82yJ4g3")    # User: 383RT, Pass: 3DQra
    WEEK2_UNCHANGED_GROUP2.append("EhAcgf8zq9EuFKzno")    # User: 499zX, Pass: ChF6e
    WEEK2_UNCHANGED_GROUP3.append("9tTYSuL75rxtevWus")    # User: cdiky, Pass: sak9m
    WEEK2_UNCHANGED_GROUP4.append("bMyY9MiyvyYuDLovJ")    # User: i5w7k, Pass: igX5Q

    WEEK2.append(WEEK2_UNCHANGED_GROUP1)
    WEEK2.append(WEEK2_UNCHANGED_GROUP2)
    WEEK2.append(WEEK2_UNCHANGED_GROUP3)
    WEEK2.append(WEEK2_UNCHANGED_GROUP4)

    # TODO Replace users
    WEEK2_IMPLICIT_GROUP1.append("vE3daNTcMj82yJ4g3")    # User: 383RT, Pass: 3DQra
    WEEK2_IMPLICIT_GROUP2.append("EhAcgf8zq9EuFKzno")    # User: 499zX, Pass: ChF6e
    WEEK2_IMPLICIT_GROUP3.append("9tTYSuL75rxtevWus")    # User: cdiky, Pass: sak9m
    WEEK2_IMPLICIT_GROUP4.append("bMyY9MiyvyYuDLovJ")    # User: i5w7k, Pass: igX5Q

    WEEK2.append(WEEK2_IMPLICIT_GROUP1)
    WEEK2.append(WEEK2_IMPLICIT_GROUP2)
    WEEK2.append(WEEK2_IMPLICIT_GROUP3)
    WEEK2.append(WEEK2_IMPLICIT_GROUP4)

    # TODO Replace users
    WEEK2_EXPLICIT_GROUP1.append("vE3daNTcMj82yJ4g3")    # User: 383RT, Pass: 3DQra
    WEEK2_EXPLICIT_GROUP2.append("EhAcgf8zq9EuFKzno")    # User: 499zX, Pass: ChF6e
    WEEK2_EXPLICIT_GROUP3.append("9tTYSuL75rxtevWus")    # User: cdiky, Pass: sak9m
    WEEK2_EXPLICIT_GROUP4.append("bMyY9MiyvyYuDLovJ")    # User: i5w7k, Pass: igX5Q

    WEEK2.append(WEEK2_EXPLICIT_GROUP1)
    WEEK2.append(WEEK2_EXPLICIT_GROUP2)
    WEEK2.append(WEEK2_EXPLICIT_GROUP3)
    WEEK2.append(WEEK2_EXPLICIT_GROUP4)

    return 1

# Export articles to JSON
def write_articles(news_collection):

    dateString = str(DATE)[:10]
    filename = FILE_NAME_NEWS + dateString + ".json"
    desired_dir = "data"
    full_path = os.path.join(desired_dir, filename)

    try:
        with open(full_path, "w") as file:
            json.dump(news_collection, file, default=json_util.default, ensure_ascii=False)

    except:
        pass

    return 1

# Export recommendations to JSON
def write_recommendations(recommendation_list):

    dateString = str(DATE)[:10]
    filename = FILE_NAME_LISTS + dateString + ".json"
    desired_dir = "data"
    full_path = os.path.join(desired_dir, filename)

    try:
        with open(full_path, "w") as file:
           json.dump(recommendation_list, file, default=json_util.default, ensure_ascii=False)

    except:
        pass

    return 1

# Read arcitles to skip scraping
def read_articles():

    news_collection = []
    temp_news_collection = []
    url_archive = []

    dateString = str(DATE)[:10]
    filename = FILE_NAME_NEWS + dateString + ".json"
    desired_dir = "data"
    full_path = os.path.join(desired_dir, filename)

    with open(full_path) as file:
        temp_news_collection = json.load(file)

    print("\nArticle Verification and Duplication Detection")
    print(len(temp_news_collection))

    for item in temp_news_collection:
        if (item["url"] not in url_archive):
            url_archive.append((item["url"]))
            news_collection.append(item)
        else:
            print("Duplicate article detected:")
            print(item["url"])

    print(len(news_collection))

    return news_collection

# TODO Writing
# Read user preferences for recommendations
def read_preferences():

    # For each user, returns 3 values between 0-11
    preference_list = []

    return preference_list

# Sort article IDs by category
def sort_articles(news_collection):

    article_collection = []
    article_counter = 0

    for article in news_collection:

        category = article["primaryCategory"]

        if (category == "business"):
            BUSINESS.append(article["_id"])
        elif (category == "crime"):
            CRIME.append(article["_id"])
        elif (category == "entertainment&arts"):
            ENTERTAINMENT.append(article["_id"])
        elif (category == "football"):
            FOOTBALL.append(article["_id"])
        elif (category == "health"):
            HEALTH.append(article["_id"])
        elif (category == "lifeandstyle"):
            LIFESTYLE.append(article["_id"])
        elif (category == "politics"):
            POLITICS.append(article["_id"])
        elif (category == "science"):
            SCIENCE.append(article["_id"])
        elif (category == "sport"):
            SPORT.append(article["_id"])
        elif (category == "technology"):
            TECHNOLOGY.append(article["_id"])
        elif (category == "uk news"):
            UK.append(article["_id"])
        elif (category == "world"):
            WORLD.append(article["_id"])
        else:
            FILLER.append(article["_id"])
            article_counter = article_counter - 1

        article_counter = article_counter + 1

    print("\nCaterogy Overview")

    article_collection.append(BUSINESS)
    print("Business: " + str(len(BUSINESS)))
    article_collection.append(CRIME)
    print("Crime: " + str(len(CRIME)))
    article_collection.append(ENTERTAINMENT)
    print("Entertainment: " + str(len(ENTERTAINMENT)))
    article_collection.append(FOOTBALL)
    print("Football: " + str(len(FOOTBALL)))
    article_collection.append(HEALTH)
    print("Health: " + str(len(HEALTH)))
    article_collection.append(LIFESTYLE)
    print("Lifestyle: " + str(len(LIFESTYLE)))
    article_collection.append(POLITICS)
    print("Politics: " + str(len(POLITICS)))
    article_collection.append(SCIENCE)
    print("Science: " + str(len(SCIENCE)))
    article_collection.append(SPORT)
    print("Sport: " + str(len(SPORT)))
    article_collection.append(TECHNOLOGY)
    print("Technology: " + str(len(TECHNOLOGY)))
    article_collection.append(UK)
    print("UK: " + str(len(UK)))
    article_collection.append(WORLD)
    print("World: " + str(len(WORLD)))

    print("\nArticles for recommendations: " + str(article_counter))
    print("Articles for filler: " + str(len(FILLER)))

    return article_collection

# TODO Rewriting (int as input to define size of return list)
# Select two random article IDs form each category
def randomize_articles(article_collection):

    article_recommendations = []

    print("\nRandomized Article Assignment")
    for category in article_collection:

        print(category)        
        random_value_1 = 0
        random_value_2 = 1

        if (len(category) == 0):
            print("0 articles available.")
        
        elif (len(category) == 1):
            print("1 article available.")
            article_recommendations.append(category[random_value_1])

        elif (len(category) == 2):
            print("2 articles avalable.")
            article_recommendations.append(category[random_value_1])
            article_recommendations.append(category[random_value_2])

        else:
            print("3 or more articles available")
            max_value = len(category) - ARTICLE_PER_CATEGORY
            random_value_1 = random.randint(0, max_value)
            random_value_2 = random_value_1 + 1

            article_recommendations.append(category[random_value_1])
            article_recommendations.append(category[random_value_2])

    random.shuffle(article_recommendations)
    random.shuffle(FILLER)
    print(article_recommendations)

    return article_recommendations

# TODO Testing
# Select the news items from the categories the user prefers
def personalize_articles(user_preferences, article_selection):

    personalized_article_selection = []

    for i in range(0, len(user_preferences)):
        personalized_article_selection.append(article_selection[user_preferences[i]])

    return personalized_article_selection

# Create a recommendation for a user
def create_recommendation(user, article_id, prediction):

    recommendation = {
        "_id": ObjectId(),
        "userId": user,
        "articleId": article_id,
        "recommendationAlgorithm": ALGORITHM,
        "prediction": prediction,
        "createdAt": datetime.now()
    }

    return recommendation

# Create a recommendation list for each user
def assign_articles(random_articles, pos_1, pos_5, user):

    user_recommendations = []
    prediction = 0
    count = 0
    filler = 0

    # Create recommendations for all random articles
    for i in range(0, TOTAL_ARTICLES):

         # First nudged article
        if (i == POSITION_1 - 1):
            prediction = TOP_POSITION - i
            user_recommendations.append(create_recommendation(user, pos_1, prediction))
        
        # Second nudged article
        elif (i == POSITION_2 - 1):
            prediction = TOP_POSITION - i
            user_recommendations.append(create_recommendation(user, pos_5, prediction))
        
        # Use random category picks to fill the list
        else:

            # Use filler to populate the feed is there are not enough articles
            if (i >= len(random_articles)):
                if (filler >= len(FILLER)):
                    break
                article_id = FILLER[filler]
                filler = filler + 1
            else: 
                article_id = random_articles[count]

            count = count + 1
            prediction = TOP_POSITION - i
            user_recommendations.append(create_recommendation(user, article_id, prediction))

    return user_recommendations

# Run scraper
def run_scrapers():

    news_collection = []
    outlet_collection = []

    # OK
    print("\nRunning BBC scraper...")
    outlet_collection.append(bbc.scrape())

    # OK
    print("\nRunning Guardian scraper...")
    outlet_collection.append(guardian.scrape())

    # OK
    print("\nRunning Independent scraper...")
    outlet_collection.append(independent.scrape())

    # OK
    print("\nRunning iNews scraper...")
    outlet_collection.append(inews.scrape())

    # OK
    print("\nRunning Sky scraper...")
    outlet_collection.append(sky.scrape())

    # OK
    print("\nRunning Standard scraper...")
    outlet_collection.append(standard.scrape())

    for outlet in outlet_collection:
        for article in outlet:
            news_collection.append(article)

    return news_collection

# Run recommender for week 1
def run_recommender(article_selection):

    recommendation_list = []
    user_list = []

    # V2 of the recommendation script
    print("\nCreating Recommendation")
    for group in WEEK1:
        for user in group:
            if (group == WEEK1_GROUP1):
                user_recommendations = assign_articles(article_selection, ENV_OG, POPULAR, user) 
            elif (group == WEEK1_GROUP2):
                user_recommendations = assign_articles(article_selection, ENV_RW, POPULAR, user)
            elif (group == WEEK1_GROUP3):
                user_recommendations = assign_articles(article_selection, POPULAR, ENV_OG, user)
            elif (group == WEEK1_GROUP4):
                user_recommendations = assign_articles(article_selection, POPULAR, ENV_RW, user)
            user_list.append(user_recommendations)
            #print(len(user_recommendations))

    # V1 of the recommendation script
    # for user in WEEK1_GROUP1:
    #     user_recommendations = assign_articles(article_selection, ENV_OG, POPULAR, user)
    #     user_list.append(user_recommendations)
    #     #print(len(user_recommendations))

    # for user in WEEK1_GROUP2:
    #     user_recommendations = assign_articles(article_selection, ENV_RW, POPULAR, user)
    #     user_list.append(user_recommendations)
    #     #print(len(user_recommendations))

    # for user in WEEK1_GROUP3:
    #     user_recommendations = assign_articles(article_selection, POPULAR, ENV_OG, user)
    #     user_list.append(user_recommendations)
    #     #print(len(user_recommendations))

    # for user in WEEK1_GROUP4:
    #     user_recommendations = assign_articles(article_selection, POPULAR, ENV_RW, user)
    #     user_list.append(user_recommendations)
    #     #print(len(user_recommendations))

    for user in user_list:
        for item in user:
            recommendation_list.append(item)

    print("Number of recommendations: " + str(len(recommendation_list)))

    return recommendation_list

# TODO Writing
# Run personalized recommender for week 2
def run_personalized_recommender(article_selection, preference_list):

    recommendation_list = []
    user_list = []
    user_count = 0

    print("\nCreating Recommendation")
    for group in WEEK2:
        for user in group:
            personalized_article_selection = personalize_articles(preference_list[user_count], article_selection)

            # Condition 1: Unchanged recommendations
            if (group == WEEK2_UNCHANGED_GROUP1):
                user_recommendations = assign_articles(article_selection, ENV_OG, POPULAR, user) 
            elif (group == WEEK2_UNCHANGED_GROUP2):
                user_recommendations = assign_articles(article_selection, ENV_RW, POPULAR, user)
            elif (group == WEEK2_UNCHANGED_GROUP3):
                user_recommendations = assign_articles(article_selection, POPULAR, ENV_OG, user)
            elif (group == WEEK2_UNCHANGED_GROUP4):
                user_recommendations = assign_articles(article_selection, POPULAR, ENV_RW, user)
  
            # Condition 2: Implicit recommendations
            elif (group == WEEK2_IMPLICIT_GROUP1):
                user_recommendations = assign_articles(personalized_article_selection, ENV_OG, POPULAR, user)
            elif (group == WEEK2_IMPLICIT_GROUP2):
                user_recommendations = assign_articles(personalized_article_selection, ENV_RW, POPULAR, user)
            elif (group == WEEK2_IMPLICIT_GROUP3):
                user_recommendations = assign_articles(personalized_article_selection, POPULAR, ENV_OG, user)
            elif (group == WEEK2_IMPLICIT_GROUP4):
                user_recommendations = assign_articles(personalized_article_selection, POPULAR, ENV_RW, user)
        
            # Condition 3: Explicit recommendations
            elif (group == WEEK2_EXPLICIT_GROUP1):
                user_recommendations = assign_articles(personalized_article_selection, ENV_OG, POPULAR, user)
            elif (group == WEEK2_EXPLICIT_GROUP2):
                user_recommendations = assign_articles(personalized_article_selection, ENV_RW, POPULAR, user)
            elif (group == WEEK2_EXPLICIT_GROUP3):
                user_recommendations = assign_articles(personalized_article_selection, POPULAR, ENV_OG, user)
            elif (group == WEEK2_EXPLICIT_GROUP4):
                user_recommendations = assign_articles(personalized_article_selection, POPULAR, ENV_RW, user)

            user_list.append(user_recommendations)
            #print(len(user_recommendations))

    for user in user_list:
        for item in user:
            recommendation_list.append(item)

    print("Number of recommendations: " + str(len(recommendation_list)))

    return recommendation_list

# Run combined script of scrapers and recommender
def main():

    # Creating arrays for week 1 and 2
    article_selection = []                      # Array with 2 news items per category
    preference_list = []                        # Array with 3 favorite categories per user
    recommendation_list = []                    # Array with all user recommendations
 
    # Step 1: Run scraper
    news_collection = run_scrapers()
    write_articles(news_collection)
    news_collection = read_articles()

    # Step 2: Run recommender
    article_collection = sort_articles(news_collection)

    # Setup for week 1
    if (WEEK == 1):
        setup_week_1()
        article_selection = randomize_articles(article_collection)
        recommendation_list = run_recommender(article_selection)

    # Setup for week 2
    elif (WEEK == 2):
        setup_week_2()
        preference_list = read_preferences()
        # TODO Rewrite
        article_selection = randomize_articles(article_collection)
        recommendation_list = run_personalized_recommender(article_selection, preference_list)

    write_recommendations(recommendation_list)

    return 1

# Run scraper and recommender script
main()
