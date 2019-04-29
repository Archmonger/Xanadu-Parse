import requests
import feedparser
import re
from Standardize import standardize_title


def contentSearch(contentType):
    search_dict = {}

    # Set movie/series categories
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

    # Creating an API request to xanadu.cf
    url = "https://xanadu.cf/api/v2.0/indexers/" + indexer + "/results/torznab/api"
    parameters = {"apikey": "7o0tagxqeryipw4oqbbn1je2az11qnph", "cat": cat, "q": input("Search Query: ")}
    response = requests.get(url, parameters)

    if response.status_code == 200:
        # Parsing the contents of the request (RSS feed) into human-readable format using feedparser
        rss = feedparser.parse(response.content)
        for post in rss.entries:
            title = standardize_title(post.title)

            if title is not None and title not in search_dict:
                search_dict[title] = post.comments

        # Print all titles
        for title, link in search_dict.items():
            print(title)

    else:
        print("Connection Failed!")


def main():
    continueProgram = True;
    while continueProgram:
        contentType = input("(M)ovie, (S)eries, or categories: ").lower()
        if contentType == 'm' or contentType == 's' or contentType[0].isnumeric():
            contentSearch(contentType)
        else:
            print("Incorrect input!")

        if input('Do you want to continue: ').lower() in ('n', 'no'):
            continueProgram = False


if (__name__ == "__main__"):
    main()