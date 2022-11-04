from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

articles = []
for p in range(1, 3):
    url = f'https://news.ycombinator.com/news?p={p}'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    for tr in soup.find_all('tr', class_='athing'):
        rank = tr.find('td', class_='title').text.replace('.', '')
        a = tr.find('a', class_='storylink')
        link = a.get('href')
        title = a.text
        next_tr = tr.find_next_sibling('tr')
        score = next_tr.find('span', class_='score')
        score = re.sub(' point(s)', '', score.get_text()) if score else '0'
        # find the comments count via the regex pattern
        # (a digit followed by &nbsp; followed by comments or comment)
        comments = next_tr.find('a', string=re.compile('\d+(&nbsp;|\s)comment(s?)'))
        comment_counts = re.sub('\xa0comment(s?)', '', comments.get_text()) if comments else 0
        comment_link = comments.get('href') if comment_counts else None
        comment_link = f"https://news.ycombinator.com/{comment_link}" if comment_link else None
        articles.append({
            'rank': rank,
            'title': title,
            'link': link,
            'score': score,
            'comment_counts': comment_counts,
            'comment_link': comment_link
        })

csvfile = pd.DataFrame.from_dict(articles)
csvfile.to_csv('hn_articles.csv', index=False)
