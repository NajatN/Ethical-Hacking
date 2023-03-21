import sys
import requests
import re
import urllib.parse
import itertools

def main():
    if len(sys.argv) < 4:
        print("Not enough arguments! You need to input 3 arguments(url,subdomains input file, directories and files input file)!")
        sys.exit(1)
        
    target = sys.argv[1]
    subs_input_file = sys.argv[2]
    dirs_input_file = sys.argv[3]
        
if __name__ == '__main__':
    main()
