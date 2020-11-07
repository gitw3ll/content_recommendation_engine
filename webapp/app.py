
# export FLASK_APP=app
# export FLASK_ENV=development
# flask run

# https://elemental.medium.com/10-signs-the-pandemic-is-about-to-get-much-worse-cf261bf3885d

import json
from text_scorer import ColorScorer
from flask import Flask, render_template, request

from database.database import get_db_connection

COLOR_DICT = {
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

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/color_score', methods=['POST'])
def color_scorer():
    print(f'Starting Color Scorer...')
    url = request.form["url"]
    print(f'url: {url}')

    cs = ColorScorer(COLOR_DICT)
    results = cs.calculate_color_score(url)
    
    # Inserting results into database
    conn = get_db_connection('database/database.db')
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