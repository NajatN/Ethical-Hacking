import sys
import requests
import re
import urllib.parse
import itertools

def getHtml(url):
    try:
        response = requests.get(url)
    except Exception as e:
        print(e)
        sys.exit(1)
    # A list of encodings to try in order
    encodings = ['utf-8', 'iso-8859-1', 'windows-1252']
    # Try each encoding until one works
    for encoding in encodings:
        try:
            html = response.content.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    return html


def main():
    if len(sys.argv) < 4:
        print("Not enough arguments! You need to input 3 arguments(url,subdomains input file, directories and files input file)!")
        sys.exit(1)
        
    target = sys.argv[1]
    subs_input_file = sys.argv[2]
    dirs_input_file = sys.argv[3]
        
if __name__ == '__main__':
    main()
