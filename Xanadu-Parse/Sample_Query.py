import requests
import feedparser
import re
import sys


def standardize_title(title):
    if title.count(' ') <= 1:
            # Standardize periods to spaces
            if title.count('.') > 0 and title.count('.') > title.count('_'):
                a = re.compile(r"\w\.\.") # abc..  ->  abc .
                b = re.compile(r"\.\.\w") # ..abc  ->  . abc
                c = re.compile(r"\w\.\w") # abc.abc  ->  abc abc
                # " mp4" -> .mp4
                d = re.compile(
                    r" (mkv|mp4|m4p|m4v|mpg|mp2|mpeg|mpe|mpv|svi|divx|flv|f4v|f4p|f4a|f4b|avi|wmv|mov|webm|vob|yuv)$")
                for match in a.finditer(title):
                    title = title[:match.start()+1] + " " + title[match.start()+2:]
                for match in b.finditer(title):
                    title = title[:match.start()+1] + " " + title[match.start()+2:]
                for match in c.finditer(title):
                    title = title[:match.start()+1] + " " + title[match.start()+2:]
                for match in d.finditer(title):
                    title = title[:match.start()] + "." + title[match.start()+1:]

            # Standardize underscores to spaces
            elif title.count('_') > 0:
                title = title.replace("_", " ")

    return title


def main():
    # loads search query into string
    # needed because each word is passed in as a separate value
    c = 0
    search_string = ""
    for x in sys.argv:
        if c == 1:
            if x == "tv":
                cat = "5000,5030,5040,5060,5070"
            else:
                cat = "2000,2020,2040,2050,2070"
        elif c > 1:
            search_string += x + " "
        elif c == sys.argv.__sizeof__():
            search_string += x
        c += 1

    # Creating an API request to xanadu.cf
    parameters = {"apikey": "7o0tagxqeryipw4oqbbn1je2az11qnph", "cat": cat, "q": search_string}
    url = "https://xanadu.cf/api/v2.0/indexers/all/results/torznab/api"
    response = requests.get(url, parameters)

    if response.status_code == 200:
        # Parsing the contents of the request (RSS feed) into human-readable format using feedparser
        rss = feedparser.parse(response.content)

        results_file = open("results.txt", 'w')
        for post in rss.entries:
            t = standardize_title(post.title)
            print(t + " " + post.comments)
            print(t, file=results_file)
            print(post.comments, file=results_file)
    else:
        input("Connection Failed!")


if __name__ == "__main__":
    main()
