import string
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords, wordnet
nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer


def process_text(text):
    """
        1. Lowercase text
        2. Removes weird characters
        3. Removes punctuation
        4. Removes digits
        5. Removes stopwords
        6. Lemmatizes remaining words
    """

    text = text.lower()

    for char in ['\n', '“', '”']:
        text = text.replace(char, '')

    text = text.rstrip('written bywritten by')
    text = text.translate(str.maketrans('', '', string.punctuation))

    nopunc_digit = [char for char in text if char not in string.punctuation and not char.isdigit()]
    nopunc_digit = ''.join(nopunc_digit)

    wnl = WordNetLemmatizer()
    lemmatized = [wnl.lemmatize(word) for word in nopunc_digit.split() if not wnl.lemmatize(word) in set(stopwords.words('english'))]
    lemmatized = ' '.join(lemmatized)
    
    return lemmatized

def get_synonyms(word):
    """
        Returns a list of synonyms for the word
    """
    return [lemma.name() for synset in wordnet.synsets(word) for lemma in synset.lemmas()]