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
    
def cleanDirsAndFiles(dirs_file):
    try:
        with open(dirs_file) as file:
            directories_and_files_to_check = file.read().splitlines()
            directories_and_files_to_check = [re.sub(r'\s+', '', directory) for directory in directories_and_files_to_check]
            directories_and_files_to_check = [re.sub(r'^/|/$', '', directory) for directory in directories_and_files_to_check]
    except IOError as e:
        print(f"Error: {e}")
    return directories_and_files_to_check

def getLinks(url):
    correct_links=[]
    links_pattern = r'<a[^>]+href=[\"|\']([^\"\']+)[\"|\'][^>]*>'
    html=getHtml(url)
    links=re.findall(links_pattern,html)
    for link in links:
        if link.startswith("http"):
            response = requests.get(link)
            if response.status_code >= 200 and response.status_code <= 299:
                correct_links.append(link)
    return correct_links
    
def getSubdomains(subdomains_to_check,url_components):
    correct_subdomains = set()
    valid_Links=[]
    for subdomain in subdomains_to_check:
        if url_components.netloc.startswith("www"):
            url_to_check = f"{url_components.scheme}://www.{subdomain}.{url_components.netloc[4:]}"
        else:
            url_to_check = f"{url_components.scheme}://{subdomain}.{url_components.netloc}"
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
    try:
        with open("subdomains_output.bat", "w") as file:
            file.write("\n".join(correct_subdomains))
    except IOError as e:
        print(f"Error: {e}")
    return valid_Links

def getDirsAndFiles(directories_and_files_to_check,target):
    correct_directories_and_files = set()
    valid_Links=[]
    for directory_or_file in directories_and_files_to_check:
        url_to_check = f"{target}/{directory_or_file}"
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
    try:
        with open("directories_and_files_output.bat", "w") as file:
            file.write("\n".join(correct_directories_and_files))
    except IOError as e:
        print(f"Error: {e}")
    return valid_Links

def writeLinksToFile(correct_links):
    flat_links = list(itertools.chain.from_iterable(correct_links))
    try:
        with open("links_output.bat", "a") as file:
            file.write("\n".join(flat_links))
    except IOError as e:
        print(f"Error: {e}")

def main():
    if len(sys.argv) < 4:
        print("Not enough arguments! You need to input 3 arguments(url,subdomains input file, directories and files input file)!")
        sys.exit(1)
        
    target = sys.argv[1]
    subs_input_file = sys.argv[2]
    dirs_input_file = sys.argv[3]
    
    html=getHtml(target)
    url_components = urllib.parse.urlsplit(target)
    
    subdomains_to_check = cleanSubdomains(subs_input_file)
    directories_and_files_to_check = cleanDirsAndFiles(dirs_input_file)
    
    links1=getSubdomains(subdomains_to_check,url_components)
    writeLinksToFile(links1)
    links2=getDirsAndFiles(directories_and_files_to_check,target)
    writeLinksToFile(links2)
        
if __name__ == '__main__':
    main()
