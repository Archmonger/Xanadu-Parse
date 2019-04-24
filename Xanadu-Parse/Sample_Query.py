import requests
import feedparser

# Sending an API request to xanadu.cf
parameters = {"apikey": "7o0tagxqeryipw4oqbbn1je2az11qnph", "cat": "5000,5030,5040,5060,5070,2000,2020,2040,2050,2070", "q": input("Search: ")}
url = "https://xanadu.cf/api/v2.0/indexers/all/results/torznab/api"
response = requests.get(url, parameters)
search_dict = {}

if response.status_code == 200:
    # Parsing the contents of the request (RSS feed) into human-readable format using feedparser
    rss = feedparser.parse(response.content)
    for post in rss.entries:
        search_dict[post.title] = post.comments
    for result in search_dict:
        print(result)
else:
    print("Connection Failed!")