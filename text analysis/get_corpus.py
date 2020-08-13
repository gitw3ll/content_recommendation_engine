import pandas as pd
from bs4 import BeautifulSoup
import requests

def scrape_corpus(ser):
    page_response = requests.get(str(ser))
    soup = BeautifulSoup(page_response.content, 'html.parser')
    corpus = ''
    for el in soup.find_all('p'):
        corpus += el.get_text()
    return corpus

def write_top_json(articles):
    top_articles = articles.loc[articles['claps'] >= 500].copy()
    top_articles['corpus'] = top_articles['url'].apply(scrape_corpus)
    with open('top_articles.json', 'w') as f:
        f.write(top_articles.to_json())

dir = './scraping/scraped_data/'
file = '20170101wellness20200701.json'
articles = pd.read_json(dir+file)
write_top_json(articles)