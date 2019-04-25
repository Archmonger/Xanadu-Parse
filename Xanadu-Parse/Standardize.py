import re
import sys

def standardize_title(title):
    if (title.count(' ') <= 1):
            # Standardize periods to spaces
            if (title.count('.') > 0 and title.count('.') > title.count('_')): 
                a = re.compile(r"\w\.\.") # abc..  ->  abc .
                b = re.compile(r"\.\.\w") # ..abc  ->  . abc
                c = re.compile(r"\w\.\w") # abc.abc  ->  abc abc
                d = re.compile(r" (mkv|mp4|m4p|m4v|mpg|mp2|mpeg|mpe|mpv|svi|divx|flv|f4v|f4p|f4a|f4b|avi|wmv|mov|webm|vob|yuv)$") #  mp4 -> .mp4
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

    return title;

def main():
    if (len(sys.argv) > 2):
        return "ERROR: Standardization script only accepts one arguement."
    else:
        return standardize_title(sys.argv[1])

if (__name__== "__main__"):
    main()