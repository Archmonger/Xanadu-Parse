import requests
import feedparser
import re

# Sending an API request to xanadu.cf
parameters = {"apikey": "7o0tagxqeryipw4oqbbn1je2az11qnph", "cat": "5000,5030,5040,5060,5070,2000,2020,2040,2050,2070", "q": input("Search: ")}
url = "https://xanadu.cf/api/v2.0/indexers/all/results/torznab/api"
response = requests.get(url, parameters)
search_dict = {}

if response.status_code == 200:
    # Parsing the contents of the request (RSS feed) into human-readable format using feedparser
    rss = feedparser.parse(response.content)
    for post in rss.entries:
        title = post.title;
        if (title.count(' ') <= 1):
            # Standardize periods to spaces
            if (title.count('.') > 0 and title.count('.') > title.count('_')): 
                a = re.compile(r"\w\.\.") # abc..  ->  abc .
                b = re.compile(r"\.\.\w") # ..abc  ->  . abc
                c = re.compile(r"\w\.\w") # abc.abc  ->  abc abc
                d = re.compile(r" (mkv|mp4|m4p|m4v|mpg|mp2|mpeg|mpe|mpv|svi|divx|flv|f4v|f4p|f4a|f4b|avi|wmv|mov|webm|vob|yuv)$") # " mp4" -> .mp4
                for match in a.finditer(title):
                    title = title[:match.start()+1] + " " + title[match.start()+2:]
                for match in b.finditer(title):
                    title = title[:match.start()+1] + " " + title[match.start()+2:]
                for match in c.finditer(title):
                    title = title[:match.start()+1] + " " + title[match.start()+2:]
                for match in d.finditer(title):
                    title = title[:match.start()] + "." + title[match.start()+1:]

            # Standardize underscores to spaces
            elif (title.count('_') > 0): 
                title = title.replace("_", " ")
            
            search_dict[title] = post.comments

    # Print all titles
    for title in search_dict:
        print(title)
else:
    print("Connection Failed!")