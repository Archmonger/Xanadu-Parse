import requests
import feedparser
import re
import sys
from Standardize import standardize_title


def contentSearch():
    search_dict = {}
    
    # Manual interface
    if len(sys.argv) != 3:
        searchQuery = input("Search Query: ")
        contentType = input("(M)ovie, (S)eries, or categories: ").lower()
        if contentType == 'm':
            cat = "2000,2020,2040,2050,2070"
        elif contentType == 's':
            cat = "5000,5030,5040,5060,5070"
        elif contentType[0].isnumeric():
            cat = contentType
        # See if the user wants a specific indexer
        indexer = input("Type in the indexer (optional): ")
        if indexer == "":
            indexer = "all";

    # CLI
    else:
        if sys.argv[1] == 'm':
            cat = "2000,2020,2040,2050,2070"
        elif  sys.argv[2] == 's':
            cat = "5000,5030,5040,5060,5070"
        indexer = "all"
        searchQuery = sys.argv[2]

    # Creating an API request to xanadu.cf
    url = "https://xanadu.cf/api/v2.0/indexers/" + indexer + "/results/torznab/api"
    parameters = {"apikey": "7o0tagxqeryipw4oqbbn1je2az11qnph", "cat": cat, "q": searchQuery}
    response = requests.get(url, parameters)

    if response.status_code == 200:
        # Parsing the contents of the request (RSS feed) into human-readable format using feedparser
        rss = feedparser.parse(response.content)
        for post in rss.entries:
            title = standardize_title(post.title)
            if title is not None and title not in search_dict:
                search_dict[title] = post.title

        # Print all titles
        results_file = open("results.txt","w+")
        for std_title, title in search_dict.items():
            print(std_title)
            print(title)
            print(std_title, file=results_file)
            print(title, file=results_file)

    else:
        print("Connection Failed!")

def main():
    contentSearch()


if (__name__ == "__main__"):
    main()