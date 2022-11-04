from bs4 import BeautifulSoup
import requests
import json

url = 'http://quotes.toscrape.com'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

items = soup.find_all('div', class_='quote')

quotes_list = []
for item in items:
    quote = item.find('span', class_='text').get_text(strip=True)
    author = item.find('small', class_='author').get_text(strip=True)
    bio = item.find('a', href=True).get('href')
    bio_link = url + bio
    a_tags = item.find('div', class_='tags').find_all('a')
    tags = [tag.get_text(strip=True) for tag in a_tags]
    quotes_dict = {
        "quote": quote.replace('\u201c', '').replace('\u201d', ''),
        "author": author,
        "bio": bio_link,
        "tags": tags
    }
    quotes_list.append(quotes_dict)
with open('quotes_info.json', 'w') as handler:
    json.dump(quotes_list, handler)