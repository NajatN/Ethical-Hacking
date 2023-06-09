# Ethical Hacking & Website Exploitation
## Description
This is a Python script that takes three arguments - a URL, a subdomains input file, and a directories and files input file - and does the following: 
* Checks the availability of subdomains by constructing URLs using given subdomains and sending a GET request to each URL.
* Checks the availability of directories and files by constructing URLs using given directories and files and sending a GET request to each URL.
* Retrieves the HTML content of the valid URLs discovered.
* Extracts links from the retrieved HTML content.
* Writes the available subdomains, directories, and files to output files.
* Writes all the links extracted from the subdomains, directories, and files to an output file.

This script is designed to perform reconnaissance on a target website by checking the availability of subdomains, directories, and files. It then extracts links from these locations and provides the information for further analysis. The information gathered can be used to identify potential vulnerabilities in the target website, which could be used to exploit it. Therefore, this script can be a useful tool for security researchers and penetration testers to test the security of websites and identify areas that need to be strengthened to prevent potential cyber attacks.

## Usage
Execute the following command on terminal after changing your current directory to the one containing the script.py file. File1 and file2 are the files comprising the subdomains to check, and the directories and files to check, respectively. In my case, I used 'subdomains_dictionary.bat' and 'dirs_dictionary.bat'. However, I didn't hardcode these specific files into my script in case it is to be tested on different input files.

Replace 'http://www.example.com' with the target website's URL.

Replace 'file1' and 'file2' with the input files you intend to read subdomains, directories, and files from.
```
python3 script.py http://www.example.com file1 file2
```

## Dependencies
This code depends on the following Python libraries:

* sys - used to access system-specific parameters and functions.
* requests - used to make HTTP requests.
* re - used for regular expressions.
* urllib.parse - used to parse URLs.
* itertools - used for working with iterators.

## Functions
- getHtml(url):

  This function takes a URL as input and returns the HTML content of the URL. It uses the requests library to make a GET request to the URL and retrieves the content. It then tries to decode the content using a list of encodings in a specific order until it finds one that works. Finally, it returns the decoded HTML content.
__________

- getLinks(url):

  This function takes a URL as input and returns a list of valid links in the HTML content of the URL. It uses a regular expression to extract links from       the HTML content. It then sends a GET request to each link and checks if the response code is valid. If it is, the link is added to a list of valid links. Finally, the function returns the list of valid links.
___________

- getSubdomains(subdomains_to_check, url_components):

  This function takes a list of subdomains to check and the URL components of the target URL as input. It constructs URLs using each subdomain and sends a GET request to the URL. If the request is successful, the subdomain is added to a set of correct subdomains. The function also calls the getLinks() function for each valid subdomain URL and returns a list of all the valid links extracted from the subdomains.
____________

- getDirsAndFiles(directories_and_files_to_check, target):

  This function takes a list of directories and files to check and the target URL as input. It constructs URLs using each directory or file and sends a GET request to the URL. If the request is successful, the directory or file is added to a set of correct directories and files. The function also calls the getLinks() function for each valid directory or file URL and returns a list of all the valid links extracted from the directories and files.
____________

- cleanSubdomains(subs_file):

  This function takes a subdomains input file as input and returns a list of cleaned subdomains. It reads the subdomains from the input file, removes any whitespace, and removes any characters that are not alphanumeric, hyphen, or period.
____________

- cleanDirsAndFiles(dirs_file):

  This function takes a directories and files input file as input and returns a list of cleaned directories and files. It reads the directories and files from the input file, removes any whitespace, and removes any leading or trailing forward slashes.
____________

- writeLinksToFile(correct_links):

  This function takes a list of valid links as input and writes them to an output file.
____________

- writeFlatLinksToFile(correct_links):

  This function takes a list of lists of valid links as input and writes them to an output file. It flattens the list of lists into a single list of strings and writes them to the output file.

## Challenges :warning:
- Downloading requests library:

  One of the initial challenges I faced was downloading the Requests library, which is a crucial tool for sending HTTP requests in Python. At first, I tried to download the 'requests' package through the command prompt, but it didn't work. I then tried to install it using pip, but still encountered issues. Finally, I downloaded the package manually from the official website, which actually worked.
_______________________________

- Dealing with UnicodeDecodeError:
  
  I also encountered the UnicodeDecodeError when decoding the HTML content of various websites meant for testing ethical hacking. To overcome this challenge, the getHtml() function tries each encoding until it succeeds or runs out of encodings to try.
_______________________________

- Encountering several exceptions:

  Another problem I faced was encountering several exceptions and having the code stop abruptly during the execution. This happened mainly when I was sending GET requests to certain endpoints, which could result in a variety of errors such as connection errors, timeouts, or invalid responses. To resolve this, I included a try-except block when sending a GET request, which allowed the program to catch and handle any exceptions that may occur.
________________________________

- Managing code:
  
  One of the main challenges while developing the code for this project was that it quickly became very messy and difficult to manage. There were several repetitive sections of code that made it hard to read and maintain, and the logic was scattered throughout the script. To overcome this problem, I decided to refactor the code by creating functions to encapsulate common tasks and simplify the main logic. By breaking down the code into smaller, reusable parts, I was able to make it more organized and easier to understand.
________________________________

- Constructing URLs for subdomains:

  I faced the challenge of properly constructing URLs for subdomains in the getSubdomains() function. This was overcome by using the netloc attribute of the urllib.parse.urlparse() function to get the domain name from the URL and then constructing the subdomain URL using the obtained domain name.
________________________________

- Using Metasploit to test script:

  Finally, I faced a challenge when trying to test my script using Metasploit, a popular penetration testing framework. Upon researching, I found out that Metasploit does not provide websites for testing scripts, but rather Metasploitable is designed for that purpose. However, my attempts to install Metasploitable were unsuccessful. As a workaround, I resorted to using websites like 'tryhackme.com' to test my script.


