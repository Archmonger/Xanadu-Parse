import requests
import feedparser
import sys

# loads search query into string
# needed because each word is passed in as a separate value
c = 0
search_string = ""
for x in sys.argv:
    if c >= 1:
        search_string += x + " "
    if c == sys.argv.__sizeof__():
        search_string += x
    c += 1


# Sending an API request to xanadu.cf
parameters = {"apikey": "7o0tagxqeryipw4oqbbn1je2az11qnph", "cat": "5000,5030,5040,5060,5070,2000,2020,2040,2050,2070",
              "q": search_string}
url = "https://xanadu.cf/api/v2.0/indexers/all/results/torznab/api"
response = requests.get(url, parameters)
search_list = []

if response.status_code == 200:
    # Parsing the contents of the request (RSS feed) into human-readable format using feedparser
    rss = feedparser.parse(response.content)

    results_file = open("results.txt", 'w')
    for post in rss.entries:
        print(post.title + " " + post.comments)
        print(post.title, file=results_file)
        print(post.comments, file=results_file)

else:
    print("Connection Failed!")
