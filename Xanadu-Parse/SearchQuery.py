import requests
import feedparser
import re
import sys
import csv
from Standardize import standardize_title


def contentSearch():
    search_results = {}
    
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
        elif sys.argv[1] == 's':
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

        # Ensure no duplication, and validate category.
        csv_reader = csv.DictReader(open('AITestFile.csv'), delimiter='|', quotechar='"')  
        parse_history = []
        for row in csv_reader:
            parse_history.append(row['Altered File Name'])
        for post in rss.entries:
            title = standardize_title(post.title)
            if title is not None and title not in search_results and title not in parse_history and "tags" in post:
                search_results[title] = post.title
                #print(title)
                #print(post.jackettindexer["id"])
                #for tags in post.tags:
                #    print(tags.term + " ", end='')
                #print()

            # If an issue was detected, report it to console.
            else:
                print(">>> Rejected Start <<< ")
                if title is not None:
                    print("Title: " + title)
                else:
                    print("Title: " + post.title)
                print("Indexer: " + post.jackettindexer["id"])

                if title is None:
                    print("Title uses non-ACSII characters.")
                if title in search_results:
                    print("Standardized title is already in search results.")
                if title in parse_history:
                    print("Standardized title is already in parse history.")
                if "tags" not in post:
                    print("Post contains no category tags.")            

                print(">>> Rejected End <<<")

        # Save titles to file
        results_file = open("results.txt","w+")
        for std_title, title in search_results.items():
            print(std_title, file=results_file)
            print(title, file=results_file)

    else:
        print("Connection Failed!")

def main():
    contentSearch()


if (__name__ == "__main__"):
    main()