import sys
import requests
import re
import urllib.parse
import itertools

def getHtml(url):
# This function sends an HTTP GET request to a given URL, and tries to decode
# the response using different character encodings until it succeeds or runs
# out of encodings to try
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

def cleanSubdomains(subs_file):
# This function reads a file containing a list of subdomains to check, cleans
# them up by removing any whitespace or special characters, and returns the
# cleaned list.
    try:
        with open(subs_file) as file:
            subdomains_to_check = file.read().splitlines()
            subdomains_to_check = [re.sub(r'\s+', '', subdomain) for subdomain in subdomains_to_check]
            subdomains_to_check = [re.sub(r'[^\w.-]', '', subdomain) for subdomain in subdomains_to_check]
    except IOError as e:
        print(f"Error: {e}")
    return subdomains_to_check
    
def cleanDirsAndFiles(dirs_file):
# This function reads a file containing a list of directories and files to check,
# cleans them up by removing any whitespace or trailing slashes, and returns the
# cleaned list.
    try:
        with open(dirs_file) as file:
            directories_and_files_to_check = file.read().splitlines()
            directories_and_files_to_check = [re.sub(r'\s+', '', directory) for directory in directories_and_files_to_check]
            directories_and_files_to_check = [re.sub(r'^/|/$', '', directory) for directory in directories_and_files_to_check]
    except IOError as e:
        print(f"Error: {e}")
    return directories_and_files_to_check

def getLinks(url):
# This function gets all the links (hrefs) in the HTML content of a given URL.
# It filters out links that don't start with "http", and only keeps links
# that return a successful HTTP status code when requested.
    correct_links=[]
    links_pattern = r'<a[^>]+href=[\"|\']([^\"\']+)[\"|\'][^>]*>'
    html=getHtml(url)
    links=re.findall(links_pattern,html)
    for link in links:
        if link.startswith("http"):
            try:
                response = requests.get(link)
                # Check if the response code is valid
                if response.status_code >= 200 and response.status_code <= 299:
                    correct_links.append(link)
            except Exception as e:
                continue
    return correct_links
    
def getSubdomains(subdomains_to_check,url_components):
# This function generates URLs for all the subdomains in a given list, and tries
# to request each of them. It saves the URLs that return a successful HTTP status
# code, and also finds all the links in the HTML content of each successful URL.
# Finally, it writes the successful subdomains to a file, and returns a list of
# links found in the successful subdomains.
    correct_subdomains = set()
    valid_Links=[]
    for subdomain in subdomains_to_check:
        # Construct the URL using the subdomain
        if url_components.netloc.startswith("www"):
            url_to_check = f"{url_components.scheme}://www.{subdomain}.{url_components.netloc[4:]}"
        else:
            url_to_check = f"{url_components.scheme}://{subdomain}.{url_components.netloc}"
        # Send a get request to the URL
        try:
            response = requests.get(url_to_check)
            if response.status_code>=200 and response.status_code<=299:
                correct_subdomains.add(subdomain)
                print("Found! ",url_to_check)
                valid_Links.append(getLinks(url_to_check))
            else:
                print("Not found! ", url_to_check)
        except Exception as e:
                print("Not found! ", url_to_check)
    # Write the valid subdomains to the output file
    try:
        with open("subdomains_output.bat", "w") as file:
            file.write("\n".join(correct_subdomains))
    except IOError as e:
        print(f"Error: {e}")
    return valid_Links

def getDirsAndFiles(directories_and_files_to_check,target):
# This function generates URLs for all the directories and files in a given list, and tries
# to request each of them. It saves the URLs that return a successful HTTP status
# code, and also finds all the links in the HTML content of each successful URL.
# Finally, it writes the successful directories and files to a file, and returns a list of
# links found in the successful directories and files.
    correct_directories_and_files = set()
    valid_Links=[]
    for directory_or_file in directories_and_files_to_check:
        # Construct the URL using the directory or file
        url_to_check = f"{target}/{directory_or_file}"
        # Send a get request to the URL
        try:
            response = requests.get(url_to_check)
            if response.status_code>=200 and response.status_code<=299:
                correct_directories_and_files.add(directory_or_file)
                print("Found! ",url_to_check)
                valid_Links.append(getLinks(url_to_check))
            else:
                print("Not found! ", url_to_check)
        except Exception as e:
                print("Not found! ", url_to_check)
    # Write the valid directories and files to the output file
    try:
        with open("directories_and_files_output.bat", "w") as file:
            file.write("\n".join(correct_directories_and_files))
    except IOError as e:
        print(f"Error: {e}")
    return valid_Links

def writeLinksToFile(correct_links):
# This function takes in a list of lists of valid links (as returned by
# the `getSubdomains` and `getDirsAndFiles` functions), flattens the list
# into a single list of links, and writes them to an output file.
    flat_links = list(itertools.chain.from_iterable(correct_links))
    try:
        with open("links_output.bat", "a") as file:
            file.write("\n".join(flat_links))
    except IOError as e:
        print(f"Error: {e}")

def main():
    # Check if there are enough arguments to proceed
    if len(sys.argv) < 4:
        print("Not enough arguments! You need to input 3 arguments(url,subdomains input file, directories and files input file)!")
        sys.exit(1)
        
    # Get target URL and input files for subdomains and directories/files
    target = sys.argv[1]
    subs_input_file = sys.argv[2]
    dirs_input_file = sys.argv[3]
    
    # Retrieve HTML content and split URL into components
    html=getHtml(target)
    url_components = urllib.parse.urlsplit(target)
    
    # Extract subdomains and directories/files to check
    subdomains_to_check = cleanSubdomains(subs_input_file)
    directories_and_files_to_check = cleanDirsAndFiles(dirs_input_file)
    
    # Find links for subdomains and directories/files
    links1=getSubdomains(subdomains_to_check,url_components)
    links2=getDirsAndFiles(directories_and_files_to_check,target)
    
    # Write links to output file
    writeLinksToFile(links1)
    writeLinksToFile(links2)
        
if __name__ == '__main__':
    main()
