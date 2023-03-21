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
    encodings = ['utf-8', 'iso-8859-1', 'windows-1252']
    for encoding in encodings:
        try:
            html = response.content.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    return html

def cleanSubdomains(subs_file):
    try:
        with open(subs_file) as file:
            subdomains_to_check = file.read().splitlines()
            subdomains_to_check = [re.sub(r'\s+', '', subdomain) for subdomain in subdomains_to_check]
            subdomains_to_check = [re.sub(r'[^\w.-]', '', subdomain) for subdomain in subdomains_to_check]
    except IOError as e:
        print(f"Error: {e}")
    return subdomains_to_check

def main():
    if len(sys.argv) < 4:
        print("Not enough arguments! You need to input 3 arguments(url,subdomains input file, directories and files input file)!")
        sys.exit(1)
        
    target = sys.argv[1]
    subs_input_file = sys.argv[2]
    dirs_input_file = sys.argv[3]
    
    html=getHtml(target)
    url_components = urllib.parse.urlsplit(target)
        
if __name__ == '__main__':
    main()
