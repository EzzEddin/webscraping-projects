from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.amazon.com/Best-Sellers-Kindle-Store/zgbs/digital-text'

request = Request(url, headers={'User-agent': 'Mozilla/5.0'})
html = urlopen(request)
soup = BeautifulSoup(html, 'html.parser')

books = soup.find_all('li', class_="zg-item-immersion")
for book in books:
    rank = book.find('span', class_="zg-badge-text").get_text().replace('#', '')
    print(rank)
    title = book.find('span', class_="zg-text-center-align")
    title = title.find_next_sibling('div').get_text(strip=True)
    print(title)
    span = book.find('span', class_="a-size-small a-color-base")
    if span:
        author = span.get_text(strip=True)
    else:
        author = book.find('a', class_="a-size-small a-link-child").get_text(strip=True)
    print(author)
    rating = book.find('span', class_="a-icon-alt")
    rating = rating.get_text(strip=True).replace(' out of 5 stars', '') if rating else None
    print(rating)
    price = book.find('span', class_="p13n-sc-price").get_text(strip=True)
    print(price)
