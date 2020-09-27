'''
Takes command line input of file path of text file
Returns color counts
'''
import sys
import string
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap
from math import pi
import streamlit as st
from bs4 import BeautifulSoup
import requests


# Clean text
def clean(text):
    text = text.lower()
    for char in ['\n', '“', '”']:
        text = text.replace(char, '')
    text = text.rstrip('written bywritten by')
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

# Count instances of each word
def counter_df(text):
    wordlist = text.split()
    wordfreq = {}
    for w in wordlist:
        wordfreq[w] = wordlist.count(w)
    counter = pd.DataFrame.from_dict(wordfreq, orient='index', columns = ['count'])
    counter.index.name = 'word'
    return counter.reset_index()

# Find color for word
def find_color(word):
    for key in color_db.keys():
        if word in color_db[key]:
            return key
    return ''

def plot_color_score(df):
    """
    from https://python-graph-gallery.com/390-basic-radar-chart/
    """
    # number of variables
    categories=colors
    N = len(categories)

    # We are going to plot the first line of the data frame.
    # But we need to repeat the first value to close the circular graph:
    values=df.values.tolist()
    values += values[:1]

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # Initialise the spider plot
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)

    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories, color='grey', size=8)

    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([0,5,10], ["0", "5","10"], color="grey", size=7)
    plt.ylim(-5,15)

    # Plot data
    ax.plot(angles, values, linewidth=1, linestyle='solid')

    # Fill area
    ax.fill(angles, values, 'b', alpha=0.1)
    # plt.show()
    st.pyplot(fig)


def scrape_corpus(ser):
    page_response = requests.get(str(ser))
    soup = BeautifulSoup(page_response.content, 'html.parser')
    corpus = ''
    for el in soup.find_all('p'):
        corpus += el.get_text()
    return corpus

# Color to word database
colors = ['red', 'orange', 'yellow','green', 'teal', 'blue', 'purple']
color_db = {
    'purple_negative': ['mystery', 'mysterious', 'moodiness', 'moody', 'boredom', 'bored', 'bore', 'confusion', 'confuse', 'confused', 'disconnection', 'disconnect'],
    'purple_positive': ['connection', 'connect', 'wisdom', 'wise', 'spirituality', 'spiritual', 'royalty', 'royal, ''nobility', 'noble', 'luxury', 'luxurious', 'ambition', 'ambitious', 'wealth', 'wealthy', 'awaken', 'awake'],
    'blue_negative': ['coldness', 'cold', 'masculinity', 'masculine', 'male', 'disgust', 'disgusted', 'conflict', 'conflicting', 'aggression', 'aggressive'],
    'blue_positive': ['intuition', 'imagination', 'imagine', 'tranquility', 'tranquil', 'security', 'secure', 'integrity', 'peace', 'peaceful', 'loyalty', 'loyal', 'faith', 'faithful', 'intelligence', 'intelligent'],
    'teal_negative': ['femininity', 'feminine', 'female', 'hostility', 'hostile'],
    'teal_positive': ['communication', 'communicate', 'expression', 'express', 'healing', 'heal', 'protection', 'protect', 'sophisticated', 'cleanse', 'cleansing'],
    'green_negative': ['envy', 'envious', 'jealousy', 'jealous', 'guilt', 'guilty', 'fear', 'fearful', 'scared', 'judgmental', 'judge', 'judging', 'unforgiving', 'anxiety', 'anxious'],
    'green_positive': ['compassion', 'trust', 'freshness', 'fresh', 'environment', 'new', 'money', 'fertile', 'health', 'healthy', 'grounded', 'reconnecting', 'balanced', 'balance', 'balancing'],
    'yellow_negative': ['irresponsible', 'instability', 'grief', 'grieve', 'grieving', 'grieves', 'addiction', 'addict', 'addicted', 'insecurity', 'insecure', 'depression', 'depressed'],
    'yellow_positive': ['confident', 'confidence', 'bright', 'sunny', 'energetic', 'warm', 'happy', 'happiness', 'perky', 'joy', 'joyful', 'intellect', 'intellectual'],
    'orange_negative': ['ignorance', 'ignorant', 'sluggishness', 'sluggish', 'shame', 'ashamed', 'shameful', 'compulsiveness', 'compulsive', 'loneliness', 'lonely', 'alone', 'dependence', 'dependent'],
    'orange_positive': ['courage', 'friendliness', 'friendly', 'success', 'successful', 'creativity', 'creative', 'openness', 'open', 'sexual', 'sexy', 'sex'],
    'red_negative': ['anger', 'angry', 'unsafe', 'warned', 'warn', 'warning', 'worry', 'worried', 'volatile', 'hopelessness', 'hopeless'],
    'red_positive': ['love', 'loving', 'passion', 'passionate', 'energy', 'energetic', 'power', 'powerful', 'strength', 'strong', 'heat', 'hot', 'desire', 'safe', 'safety', 'instinctive', 'instinct', 'security', 'secure', 'liberating', 'liberate']
}

#########################################################################

url = st.text_input("URL")

if url:
    text = scrape_corpus(url)

    # Clean text
    clean_corpus = clean(text)

    # Count words
    data_df = counter_df(clean_corpus)

    # Count colors
    data_df['color'] = data_df['word'].apply(find_color)
    color_df = data_df.groupby('color').sum().drop([''])['count']

    # add colors that downt show up
    for color in color_db.keys():
        if color not in color_df.index:
            color_df = color_df.append(pd.Series(0, index=[color]))

    # sum positives and negatives
    for color in colors:
        color_df[color] = color_df[color+'_positive'] - color_df[color+'_negative']
    color_df = color_df[colors]

    # Return results
    print(color_df)
    plot_color_score(color_df)
