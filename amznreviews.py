import gzip
import pandas as pd
import numpy as np
import re
import os
from string import punctuation
import nltk
import sys
import seaborn as sns


# Required to read the input files, as they are not strict Python
# These functions were provided by Julian McAuley who prepared the dataset
def getDF(inpath, filename):
    i = 0
    df = {}
    for d in parse(os.path.join(inpath, filename)):
        df[i] = d
        i += 1
    return pd.DataFrame.from_dict(df, orient='index')


def parse(path):
    # g = open(path, 'r')
    g = gzip.open(path, 'r')
    for l in g:
        yield eval(l)


# Not using a tokenizer. Using NLTK for sentiment analysis was an afterthought
def count_words(strs):
    r = re.compile(r'[{}]'.format(punctuation))
    new_strs = r.sub(' ', strs)
    return len(new_strs.split())


def save_to_csv(df, outpath, filename):
    f = open(os.path.join(outpath, filename), 'w')
    df.to_csv(f, index=False)
    f.close()


if __name__ == "__main__":
    debugging = False
    inReviewsFile = 'reviews_Musical_Instruments.json.gz'
    inMetadataFile = 'meta_Musical_Instruments.json.gz'
    outPath = os.path.abspath('data_out')
    inPath = os.path.abspath('gzip_data')
    tempPath = os.path.abspath('temp_files')
    if len(sys.argv) == 2:
        inReviewsFile = sys.argv[1]
        inMetadataFile = sys.argv[2]

    # Ingest reviews and metadata, drop irrelevant columns
    df = getDF(inPath, inReviewsFile)
    df.drop(['reviewerID', 'reviewerName', 'summary', 'unixReviewTime', 'reviewTime'],
            axis='columns',
            inplace=True)
    md = getDF(inPath, inMetadataFile)
    md.drop(['categories', 'description', 'title', 'imUrl', 'brand', 'related', 'salesRank'],
            axis='columns',
            inplace=True)
    enrich_df = pd.merge(df, md, on='asin')
    enrich_df.replace('', np.nan, inplace=True)
    enrich_df.dropna(inplace=True)

    # if debugging:
    save_to_csv(enrich_df, tempPath, 'original_merge.csv')

    # Load with
    enrich_df = pd.read_csv(tempPath, 'original_merge.csv')

    # Construct new features
    sentences = enrich_df['reviewText']

    # calculate number of characters per review
    reviewLength = sentences.str.len()
    reviewLength.name = 'reviewLength'

    # calculate number of words per review
    lser = []
    for x in sentences:
        if count_words(x) == 0:
            lser.append(0)
        else:
            lser.append(count_words(x))
    reviewWords = pd.Series((counter for counter in lser), name="reviewWords")
    enrich_df = pd.concat([enrich_df, reviewLength, reviewWords], axis=1)

    # calculate avg word length
    avgWordLength = enrich_df.reviewLength.div(enrich_df.reviewWords)
    avgWordLength.rename('avgWordLength', inplace=True)

    # Calculate expresiveness
    expresiveness = enrich_df.reviewWords.div(enrich_df.reviewWords.mean())
    expresiveness.rename('expresiveness', inplace=True)

    # Calculating overall rating delta
    ratingDelta = enrich_df.overall.div(enrich_df.overall.mean())
    ratingDelta.rename('ratingDelta', inplace=True)

    # Calculate price delta
    priceDelta = enrich_df.price.div(enrich_df.price.mean())
    priceDelta.rename('priceDelta', inplace=True)

    # Calculate usefulness
    a = list(enrich_df['helpful'].values)
    useful_res = []
    for val in a:
        val_a, val_b = str(val).split(', ')
        r = re.compile(r'[{}]'.format(punctuation))
        a_r = r.sub('', val_a).strip()
        b_r = r.sub('', val_b).strip()
        if b_r != '0':
            useful_res.append(int(a_r) / int(b_r))
        else:
            useful_res.append(0)
    usefulness = pd.Series(useful_res, name='usefulness')

    # Append all features to dataframe
    enrich_df = pd.concat([enrich_df, avgWordLength, usefulness, expresiveness,
                           ratingDelta, priceDelta], axis=1)
    enrich_df.dropna(inplace=True)

    if debugging:
        save_to_csv(enrich_df, tempPath, 'all_features_merge.csv')
        # Load with
        # enrich_df = pd.read_csv('/Users/pacoc/CS410Project/temp_files/all_features_merge.csv')

    # Sentiment Analysis
    nltk.download('vader_lexicon')
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    sentences = list(enrich_df['reviewText'])
    sia = SentimentIntensityAnalyzer()
    ss = []
    for sentence in sentences:
        ss.append(sia.polarity_scores(str(sentence))['compound'])
    sentiment = pd.Series(ss, name='sentiment')
    enrich_df['sentiment'] = sentiment

    if debugging:
        save_to_csv(enrich_df, tempPath, 'all_features_with_sentiment_merge.csv')
        # Load with
        # enrich_df = pd.read_csv('/Users/pacoc/CS410Project/temp_files/all_features_with_sentiment_merge.csv')

    # Output
    save_to_csv(enrich_df, outPath, 'all_features_with_sentiment_merge.csv')
    sns.set(font_scale=0.7)
    corr_plot = sns.heatmap(enrich_df.corr(), annot=True, cbar=False, fmt='.2f')
    fig = corr_plot.get_figure()
    fig.savefig(os.path.join(outPath, 'corrplot.png'))
    with pd.option_context('display.precision', 2):
        print(enrich_df.corr())
