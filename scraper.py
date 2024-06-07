from urllib import response
import requests
import csv
import re
import sys
from bs4 import BeautifulSoup

output_file = 'scraping.csv'

print("""
                                                                                                               
,------. ,------. ,-----. ,-----. ,--.  ,--. ,---.   ,-----.,------.   ,---.  ,------. ,------.,------.  
|  .--. '|  .---''  .--./'  .-.  '|  ,'.|  |'   .-' '  .--./|  .--. ' /  O  \ |  .--. '|  .---'|  .--. ' 
|  '--'.'|  `--, |  |    |  | |  ||  |' '  |`.  `-. |  |    |  '--'.'|  .-.  ||  '--' ||  `--, |  '--'.' 
|  |\  \ |  `---.'  '--'\'  '-'  '|  | `   |.-'    |'  '--'\|  |\  \ |  | |  ||  | --' |  `---.|  |\  \  
`--' '--'`------' `-----' `-----' `--'  `--'`-----'  `-----'`--' '--'`--' `--'`--'     `------'`--' '--' 
                                                                                                         
""")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        url = sys.argv[1]
        print(f"Scraping {url}")
    else:
        url = input("All scrapings saved in CSV file. Please enter a URL: ")

response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'})

if response.status_code == 200:
    print('Success!')
    soup = BeautifulSoup(response.content, 'html.parser')

    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Link'])

        title = soup.title.string if soup.title else 'No title'
        print(f"Title: {title}")

        print("-----------------------------")
        print("Links")
        print("-----------------------------")

        links = soup.find_all('a', href=True)
        for link in links:
            print(f"Link: {link['href']}")
            writer.writerow([f"Link: {link['href']}"])

        print("-----------------------------")
        print("Meta Tags")
        print("-----------------------------")

        meta_tags = soup.find_all('meta')
        for meta_tag in meta_tags:
            print(f"Meta Tag: {meta_tag}")
            writer.writerow([f"Meta Tag: {meta_tag}"])

        print("-----------------------------")
        print("Headers")
        print("-----------------------------")

        headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        for header in headers:
            print(f"Header: {header}")
            writer.writerow([f"Header: {header}"])

        print("-----------------------------")
        print("Emails")
        print("-----------------------------")

        emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", response.text)
        for email in emails:
            print(f"Email: {email}")
            writer.writerow([f"Email: {email}"])

        print("-----------------------------")
        print("Forms")
        print("-----------------------------")

        forms = soup.find_all('form')
        for form in forms:
            action = form.get('action')
            method = form.get('method', 'get').lower()
            inputs = form.find_all('input')
            input_names = [inp.get('name') for inp in inputs]
            print(f"Form: action={action}, method={method}, inputs={input_names}")
            writer.writerow([f"Form: action={action}, method={method}, inputs={input_names}"])

        print("-----------------------------")
        print("JavaScript Files")
        print("-----------------------------")

        scripts = soup.find_all('script', src=True)
        for script in scripts:
            print(f"JavaScript File: {script['src']}")
            writer.writerow([f"JavaScript File: {script['src']}"])

        print("-----------------------------")
        print("HTTP Headers")
        print("-----------------------------")

        for httpheader, value in response.headers.items():
            print(f"{httpheader}: {value}")
            writer.writerow([f"{httpheader}: {value}"])

        print("-----------------------------")
        print("Technologies")
        print("-----------------------------")

        technologies = []

        server_header = response.headers.get('Server', '')
        if server_header:
            technologies.append(f"Server: {server_header}")

        x_powered_by_header = response.headers.get('X-Powered-By', '')
        if x_powered_by_header:
            technologies.append(f"X-Powered-By: {x_powered_by_header}")

        libraries = {
            'jQuery': r'jquery[-\d.]*\.js',
            'React': r'react[-\d.]*\.js',
            'Angular': r'angular[-\d.]*\.js',
            'Vue': r'vue[-\d.]*\.js',
        }

        for script in scripts:
            src = script.get('src')
            for library, pattern in libraries.items():
                if re.search(pattern, src):
                    technologies.append(f"JavaScript Library: {library}")
                    break

        if soup.find_all('link', href=re.compile(r'/wp-content/')):
            technologies.append("CMS: WordPress")

        if soup.find_all('meta', content=re.compile(r'Drupal')):
            technologies.append("CMS: Drupal")

        if soup.find_all('meta', content=re.compile(r'Joomla')):
            technologies.append("CMS: Joomla")

        for tech in technologies:
            print(tech)
            writer.writerow([tech])
                
else:
    print(f'An error has occurred. {response.status_code}')

