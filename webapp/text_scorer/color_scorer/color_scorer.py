import pandas as pd
import matplotlib.pyplot as plt
import requests

from bs4 import BeautifulSoup
from math import pi
from sklearn.feature_extraction.text import CountVectorizer

from ..preprocessing import process_text

class ColorScorer:
    def __init__(self, color_dict):
        self.color_dict = color_dict
        self.color_list =list(set([x.split('_')[0] for x in self.color_dict.keys()]))

        self.color_df = None

        self.corpus = None
        self.corpus_title = None

    def find_color(self, word):
        """
        Input:
            - word: word to match to color
        Returns the color that the word matches to based on color_db
        """
        color = [key for key in self.color_dict.keys() if word in self.color_dict[key]]
        if len(color) != 0:
            return color[0]
        return ''

    def scrape_corpus(self, url):
        """
        Input: 
            - url: URL to scrape article from
        Scrapes URL and saves article title and content in memory
        """
        page_response = requests.get(str(url))
        soup = BeautifulSoup(page_response.content, 'html.parser')
        self.corpus_title = soup.find('title').text
        corpus = ''
        for el in soup.find_all('p'):
            corpus += el.get_text()
        self.corpus = corpus
        print(f'Article "{self.corpus_title}" scraped and loaded with length: {len(corpus)}!')

    def get_text_color_score(self, text):
        """
        Input:
            - text: text to calculate color score
        Returns a dictionary with the calculated color score for each color
        """
        # Create word counts and generate dataframe
        transformer = CountVectorizer(max_features=500).fit([text])
        counter = transformer.transform([text])
        word_count_df = pd.DataFrame({
            "word": transformer.get_feature_names(),
            "counts": counter.toarray()[0]
        })

        # Match and count colors
        word_count_df['color'] = word_count_df['word'].apply(self.find_color)
        all_color_df = word_count_df.groupby('color').sum().drop([''])['counts']

        # add colors that dont show up
        for color in self.color_dict.keys():
            if color not in all_color_df.index:
                all_color_df = all_color_df.append(pd.Series(0, index=[color]))

        # sum positives and negatives
        for color in self.color_list:
            all_color_df[color] = float(all_color_df[color+'_positive'] - all_color_df[color+'_negative'])
        self.color_df = all_color_df[self.color_list]
        print(f'dict(self.color_df): {dict(self.color_df)}')
        return dict(self.color_df)
        
    def calculate_color_score(self, url):
        """
        Input:
            - url: URL to scrape and calculate color score
        Returns a dictionary with the calculated color score for each color
        """
        self.scrape_corpus(url)
        clean_corpus = process_text(self.corpus)

        return self.get_text_color_score(clean_corpus)







