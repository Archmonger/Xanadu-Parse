import requests
import feedparser
import re
from Standardize import standardize_title

def main():
    continueProgram = True;
    while continueProgram:
        # Creating an API request to xanadu.cf
        parameters = {"apikey": "7o0tagxqeryipw4oqbbn1je2az11qnph", "cat": "5000,5030,5040,5060,5070,2000,2020,2040,2050,2070", "q": input("Search: ")}
        url = "https://xanadu.cf/api/v2.0/indexers/all/results/torznab/api"
        response = requests.get(url, parameters)
        search_dict = {}

        if response.status_code == 200:
            # Parsing the contents of the request (RSS feed) into human-readable format using feedparser
            rss = feedparser.parse(response.content)
            for post in rss.entries:
                title = standardize_title(post.title)
                #title = post.title

                if title is not None and title not in search_dict:
                    search_dict[title] = post.comments

            # Print all titles
            for title, link in search_dict.items():
                print(title)
                
        else:
            print("Connection Failed!")

        if input('Do you want to continue (y/n): ') in ('n', 'N', 'no', 'NO', 'No'):
            continueProgram = False

if (__name__== "__main__"):
    main()