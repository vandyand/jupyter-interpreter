
import requests
from bs4 import BeautifulSoup

url = 'http://example.com'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Print the title of the page
print(soup.title.string)
