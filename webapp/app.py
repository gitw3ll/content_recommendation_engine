
# export FLASK_APP=app
# export FLASK_ENV=development
# flask run

# https://elemental.medium.com/10-signs-the-pandemic-is-about-to-get-much-worse-cf261bf3885d

import configparser
import json
from ast import literal_eval
from flask import Flask, render_template, request

from text_scorer import ColorScorer, get_synonyms
from database.database import get_db_connection

# Loading color dictionary for word mapping
config = configparser.ConfigParser()
config_read = config.read('color_dict.cfg')
config.sections()
COLOR_DICT = literal_eval(config['DEFAULT']['color_dict'])

updated_color_dict = {}

# Adding synonyms to the dictionary
print('Updating dictionary with synonyms...')
for color in COLOR_DICT.keys():
    syn_list = []
    for word in COLOR_DICT[color]:
        syn_list.append(get_synonyms(word))
    # flatten list of lists and gets unique words
    flat_syn_list = list(set([word for sublist in syn_list for word in sublist]))
    updated_color_dict[color] = flat_syn_list
print('Finished updating!')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/color_score', methods=['POST'])
def color_scorer(update:bool=True):
    print(f'Starting Color Scorer with update: {update}...')
    url = request.form["url"]
    print(f'url: {url}')

    # Establishing database connection
    conn = get_db_connection('database/database.db')

    # Checking if results exist
    cur = conn.cursor()
    cur.execute(
        """
        SELECT *
        FROM search_db
        WHERE article_url = ?
        """,
        (url,)
        )
    
    # Getting results
    results = cur.fetchone()
    if results is not None and not update:
        print(f'Already exists in database!')
    else:
        print("No existing record found!")
        # Running analysis
        cs = ColorScorer(updated_color_dict)
        results = cs.calculate_color_score(url)
        
        print("Adding results to database...")
        # Adding results into database
        conn.execute(
            """
            INSERT INTO search_db (article_url, red, yellow, purple, green, blue, orange, teal)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                url, 
                results['red'], 
                results['yellow'], 
                results['purple'], 
                results['green'], 
                results['blue'], 
                results['orange'], 
                results['teal']
            )
        )
        conn.commit()
        conn.close()
        print('Finished adding to database!')

    return render_template('color_score_results.html', results=results)