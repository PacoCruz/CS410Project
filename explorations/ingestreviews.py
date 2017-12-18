# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 14:14:36 2017

@author: francruz

"""
import gzip
import pandas as pd
import re
import nltk
from string import punctuation


def getDF(path):
    i = 0
    df = {}
    for d in parse(path):
        df[i] = d
        i += 1
    return pd.DataFrame.from_dict(df, orient='index')


def parse(path):
    # g = open(path, 'r')
    g = gzip.open(path, 'r')
    for l in g:
        yield eval(l)

def count_words(strs):
    r = re.compile(r'[{}]'.format(punctuation))
    new_strs = r.sub(' ',strs)
    return len(new_strs.split())

def save_to_gzjson(df, path):
    f = open(path, 'w')
    df.to_json(f, compression = 'gzip')

def save_to_json(df,path):
    f = open(path, 'w')
    df.to_json(f)

def load_from_json(path):
    f = open(path, 'r')
    tempJson = pd.read_json(f)
    tempJson.sort_index(inplace=True)
    return tempJson

def save_to_csv(df, path):
    f = open(path, 'w')
    df.to_csv(f, index = False)
    f.close()


if __name__ == "__main__":
    #    df = getDF('./data/reviews_Automotive.json')
    #    md = getDF('./data/meta_Automotive.json')
    df = getDF('./data_gzip/reviews_Automotive.json.gz')
    md = getDF('./data_gzip/meta_Automotive.json.gz')
    df.drop(['reviewerID', 'reviewerName', 'summary', 'unixReviewTime'], axis='columns', inplace=True)
#     md.drop(['imUrl', 'related', 'categories', 'description', 'salesRank'], axis='columns', inplace=True)
    md.drop(['imUrl', 'related', 'categories', 'description'], axis='columns', inplace=True)
    enrich_df = pd.merge(df, md, on='asin')

    # new features
    newcol = enrich_df['reviewText']
    # calculate number of characters per review
    reviewLength = newcol.str.len()
    reviewLength.name = 'reviewLength'
    # calculate number of words per review
    lser = []
    for x in newcol:
        lser.append(count_words(x))
    reviewWords = pd.Series((counter for counter in lser), name="reviewWords")
    enrich_df = pd.concat([enrich_df,reviewLength,reviewWords], axis=1)


    # calculate avg word length
    avgWordLength = enrich_df.reviewLength.div(enrich_df.reviewWords)
    avgWordLength.rename('avgWordLength', inplace=True)

    # Calculate expresiveness
    expresiveness = enrich_df.reviewWords.div(enrich_df.reviewWords.mean())
    expresiveness.rename('expresiveness', inplace=True)

    # Calculating overall rating
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
            useful_res.append(None)
    usefulness = pd.Series(useful_res, name='usefulness')


    # Append all features to dataframe
    enrich_df = pd.concat([enrich_df, usefulness, avgWordLength, expresiveness,
                           ratingDelta, priceDelta], axis=1)

    # Remove rows with NaN, Nulls
    enrich_df.dropna(inplace=True)

    # Sample 1000 rows for Azure
    sample_set = enrich_df.sample(1000)
    save_to_csv(sample_set, '/Users/pacoc/data_out/auto_sample_1000_nostrcast.csv')

    # Save full dataframe for NLTK
    save_to_csv(enrich_df, 'C:\\Users\\francruz\\data_out\\automotive_num.csv')
    save_to_csv(enrich_df, '/Users/pacoc/data_out/automotive_num.csv')
    save_to_json(enrich_df, 'C:\\Users\\francruz\\data_out\\automotive_num.json')
    save_to_json(enrich_df, '/Users/pacoc/data_out/automotive_num.json')




    enrich_df.fillna(value='unknown', inplace=True)




    # Cast as str for use in whoosh
    enrich_df['overall'] = enrich_df['overall'].astype('str')
    enrich_df['price'] = enrich_df['price'].astype('str')
    enrich_df['reviewLength'] = enrich_df['reviewLength'].astype('str')
    enrich_df['reviewWords'] = enrich_df['reviewWords'].astype('str')
    enrich_df['avgWordLength'] = enrich_df['avgWordLength'].astype('str')
    enrich_df['expresiveness'] = enrich_df['expresiveness'].astype('str')
    enrich_df['ratingDelta'] = enrich_df['ratingDelta'].astype('str')
    enrich_df['priceDelta'] = enrich_df['priceDelta'].astype('str')
    enrich_df['usefulness'] = enrich_df['usefulness'].astype('str')


    save_to_json(enrich_df)
    save_to_csv(enrich_df)


    # save_to_gzjson(enrich_df)
    # save_to_csv(enrich_df)
