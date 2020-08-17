import pandas as pd
from bs4 import BeautifulSoup
import requests
import time

def scrape_corpus(ser):
    page_response = requests.get(str(ser))
    soup = BeautifulSoup(page_response.content, 'html.parser')
    corpus = ''
    for el in soup.find_all('p'):
        corpus += el.get_text()
    return corpus

def write_top_json(articles, tag):
    top_articles = articles.loc[articles['claps'] >= 500].copy()
    top_articles['corpus'] = top_articles['url'].apply(scrape_corpus)
    with open('top_' + tag + '_articles.json', 'w') as f:
        f.write(top_articles.to_json())

start = time.time()
dir = '../scraping/scraped_data/'
file = '20180101health20200701.json'
articles = pd.read_json(dir+file)
write_top_json(articles, 'health')
end = time.time()
print(end-start)