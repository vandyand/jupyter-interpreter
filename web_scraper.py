import requests
from bs4 import BeautifulSoup

# Sample URL to scrape
url = 'https://example.com'

def scrape_website(url):
    # Send a GET request to the URL
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        # Save the scraped content to a file
        with open('scraped_data.txt', 'w') as file:
            file.write(soup.prettify())
    else:
        print(f"Failed to access {url}")

if __name__ == '__main__':
    scrape_website(url)
