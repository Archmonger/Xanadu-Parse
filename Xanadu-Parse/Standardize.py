import re
import sys

def standardize_title(title):
    if (title.count(' ') <= 1):
        # Standardize periods to spaces
        if (title.count('.') > 1 and title.count('.') > title.count('_')): 
            title = title.replace(".", " ")

        # Standardize underscores to spaces
        elif (title.count('_') > 0): 
            title = title.replace("_", " ")

    #Minor revisions to filename
    a = re.compile(r"\s*$") # remove trailing whitespace
    b = re.compile(r"\S \(Torrent\) - \S") # remove " (Torrent) - Uploader"
    c = re.compile(r" torrent$") # remove " torrent"    
    d = re.compile(r"\S (mkv|mp4|m4p|m4v|mpg|mp2|mpeg|mpe|mpv|svi|divx|flv|f4v|f4p|f4a|f4b|avi|wmv|mov|webm|vob|yuv)$") # " mp4" -> .mp4
    for match in a.finditer(title):
        title = title[:match.start()]
    for match in b.finditer(title):
        title = title[:match.start()+1]
    for match in c.finditer(title):
        title = title[:match.start()]
    for match in d.finditer(title):
        title = title[:match.start()+1] + "." + title[match.start()+2:]

    return title;

def main():
    if (len(sys.argv) > 2):
        return "ERROR: Standardization script only accepts one arguement."
    else:
        return standardize_title(sys.argv[1])

if (__name__== "__main__"):
    main()