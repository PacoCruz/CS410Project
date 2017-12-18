import pandas as pd
import nltk
nltk.download('vader_lexicon')


docstoindex = pd.read_csv('/Users/pacoc/data_out/automotive_num.csv')
# docstoindex = pd.read_csv('c:\\Users\\francruz\\data_out\\automotive_num.csv')
# remove rows with empty values
docstoindex.dropna(inplace=True)

from nltk.sentiment.vader import SentimentIntensityAnalyzer
sentences = list(docstoindex['reviewText'])


sia = SentimentIntensityAnalyzer()
ss = []
for sentence in sentences:
    ss.append(sia.polarity_scores(str(sentence))['compound'])

sentiment = pd.Series(ss, name = 'sentiment')
docstoindex['sentiment'] = sentiment
docstoindex.to_csv('/Users/pacoc/data_out/automotive_with_sentiment_VADER.csv')
docstoindex.to_csv('C:\\Users\\francruz\\data_out\\automotive_with_sentiment_VADER.csv')