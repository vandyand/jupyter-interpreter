import requests
from bs4 import BeautifulSoup

# URL of the website to scrape
url = https://example.com

# Send a GET request to fetch the webpage content
response = requests.get(url)

# Parse the content with BeautifulSoup
soup = BeautifulSoup(response.content, html.parser)

# Find all article titles (adjust as needed based on the website structure)
titles = soup.find_all(h2)  # Assuming articles are within <h2> tags

# Save the titles to scraped_data.txt
with open(scraped_data.txt, w) as file:
    for title in titles:
        file.write(title.get_text() + n)

