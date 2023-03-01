import lyricsgenius, os, re
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import lyricsgenius
from textblob import TextBlob
from text2emotion import get_emotion
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from string import punctuation
from collections import Counter

# Create a Genius API client instance
ACCESS_TOKEN = os.environ.get('GENIUS_CLIENT_ACCESS_TOKEN')
genius = lyricsgenius.Genius(ACCESS_TOKEN)

# ------------- helper functions --------------

# Retrieve song lyrics using Genius API
def get_lyrics(title, artist):
    song = genius.search_song(title, artist)
    lyrics = song.lyrics
   
    # Remove all unnecessary text from response
    lyrics_lines = lyrics.split('\n')
    lyrics = '\n'.join(lyrics_lines[1:]) # Remove first line 
    lyrics = re.sub(r'\[.*?\]', '', lyrics) # Remove text inside square brackets
    lyrics = re.sub(r'See .*|You might also like.*|Embed', '', lyrics) # Remove footer text

    return lyrics

def get_words(title, artist):
    lyrics = get_lyrics(title, artist)
    stop_words = set(stopwords.words('english'))
   
    words = lyrics.split()
    words = [w for w in words if not w in stop_words]
    
    # stemmer = SnowballStemmer('english')
    # words = [stemmer.stem(w) for w in words]
    
    return words

 # Calculate the overall polarity score
def get_text_blob_polarity(words):
    blob = TextBlob(' '.join(words))
    polarity = blob.sentiment.polarity

    formatted_polarity = ((polarity+1)/2)*100
    return formatted_polarity

def get_emotions(words):
    return get_emotion(' '.join(words))

 # Fine tune polarity score by using word frequencies 
def tune_polarity(words):
    pos_count = neg_count = 0
    analyzer = SentimentIntensityAnalyzer()
    for word, freq in Counter(words).items():
        # scores = analyzer.polarity_scores(word)
        score = analyzer.polarity_scores(word)['compound']
        # print(word, scores['pos'], scores['neu'], scores['neg'], score)
        if score > 0:
            pos_count += score * freq
        elif score < 0:
            neg_count += score * freq

    # Calculate total number of positive and negative words
    total_pos = sum(freq for word, freq in Counter(words).items() if analyzer.polarity_scores(word)['compound'] > 0)
    total_neg = sum(freq for word, freq in Counter(words).items() if analyzer.polarity_scores(word)['compound'] < 0)

    # Calculate overall polarity percentage
    polarity = ((pos_count - neg_count) / (total_pos + total_neg)) * 100
    return polarity

def print_analysis(title, artist):
    words = get_words(title, artist)
    print("---- Analysis for: ", title, "----")

    # Identify the emotions present in the lyrics
    emotions = get_emotions(words) 
    print("Emotions: ", emotions)

    # Calculate the text blob polarity score
    polarity = get_text_blob_polarity(words) 
    print("NLTK Vader: ", round(polarity, 2))

    custom_polarity = tune_polarity(words)
    print("Word frequency & association:", round(custom_polarity, 2))

    # Calculate the average polarity score
    stronger_weight = polarity*0.65
    weaker_weight = custom_polarity*0.35
    print("Average: ", round(stronger_weight+weaker_weight, 2))
    print("-----------------------------------")

# ------------- Testing --------------

tracks = [{"title": "drivers license", "artist": "olivia rodrigo"},{"title": "living my best life", "artist": "ben rector"},{"title": "still feeling you", "artist": "couch"},{"title": "easy to love", "artist": "couch"},]

for track in tracks:
    print_analysis(track['title'], track['artist'])
