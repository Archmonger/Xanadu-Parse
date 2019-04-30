import re
import sys

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def standardize_title(title):
    if title.count(' ') <= 2 or title.count('.') >= 3 or title.count('_') >= 3:
        # Standardize periods to spaces
        if (title.count('.') > 1 and title.count('.') > title.count('_')): 
            title = title.replace(".", " ")
            f = re.compile(r"\D\d \d\D") # 5 1 to 5.1
            for match in f.finditer(title):
                title = title[:match.start()+2] + "." + title[match.start()+3:]

        # Standardize underscores to spaces
        elif (title.count('_') > 0): 
            title = title.replace("_", " ")

    # Clean up the file name
    a = re.compile(r"\s*$") # rRmove trailing whitespace
    b = re.compile(r"\S \(Torrent\) - \S") # Remove " (Torrent) - Uploader"
    c = re.compile(r" torrent$") # Remove " torrent"        
    d = re.compile(r"\S (mkv|mp4|m4p|m4v|mpg|mp2|mpeg|mpe|mpv|svi|divx|flv|f4v|f4p|f4a|f4b|avi|wmv|mov|webm|vob|yuv)$") # " mp4" -> .mp4
    for match in a.finditer(title):
        title = title[:match.start()]
    for match in b.finditer(title):
        title = title[:match.start()+1]
    for match in c.finditer(title):
        title = title[:match.start()]
    for match in d.finditer(title):
        title = title[:match.start()+1] + "." + title[match.start()+2:]

    title = title.replace("\"","") # Remove quotation marks

    if isEnglish(title):
        return title
    else:
        return None

def main():
    if (len(sys.argv) > 2):
        return "ERROR: Standardization script only accepts one arguement."
    else:
        return standardize_title(sys.argv[1])

if (__name__== "__main__"):
    main()