## Web App for Article Scoring
To run Web App:
```
export FLASK_APP=app
export FLASK_DEV=development
flask run
```
### Structure:
#### Front End
- HTML files are stored in the templates folder, which are loaded and rendered using Flask.

#### Database: SQLite
- Whenever a new search is made on an URL, the API checks the database for this URL, then returns the color scores if the URL is found. Otherwise, it will run ColorScorer and return the results, while saving the URL and color scores into the database.

#### ColorScorer
- ColorScorer works by scraping through the URL and scanning the content for keywords based on a dictionary. It will then return the scores for each category based on the positive and negative words associated with each color.

#### Color Dictionary
- The Color Dictionary is stored in the configuration file under DEFAULT and contains 7 colors, each color with a positive and negative part. Mapping of words are done through this dictionary. When the dictionary is initially loaded in, the app will update the dictionary by adding synonyms of the words in each category to broaden the word base.