# -*- coding: utf-8 -*-

import pandas as pd
import json
import http.client, urllib.request, urllib.parse, urllib.error, base64

# **********************************************
# *** Update or verify the following values. ***
# **********************************************

# Replace the accessKey string value with your valid access key.

accessKey = '****************************'

# Replace or verify the region.
#
# You must use the same region in your REST API call as you used to obtain your access keys.
# For example, if you obtained your access keys from the westus region, replace
# "westcentralus" in the URI below with "westus".
#
# NOTE: Free trial access keys are generated in the westcentralus region, so if you are using
# a free trial access key, you should not need to change this region.
uri = 'westus.api.cognitive.microsoft.com'
path = '/text/analytics/v2.0/sentiment'


def GetSentiment(documents):
    "Gets the sentiments for a set of documents and returns the information."

    headers = {'Ocp-Apim-Subscription-Key': accessKey}
    conn = http.client.HTTPSConnection(uri)
    body = json.dumps(documents)
    conn.request("POST", path, body, headers)
    response = conn.getresponse()
    return response.read()


# Load the dataframe from csv
docstoindex = pd.read_csv('/Users/pacoc/data_out/auto_sample_1000_nostrcast.csv', dtype='str')
# Reduce to 20 docs just for test
# docstoindex.sample(20)
# docstoindex.drop(docstoindex.index[20:], inplace=True)
# Drop column not needed for sentiment analysis
docstoindex.drop(columns=['asin', 'helpful', 'overall'
    , 'reviewTime', 'title'
    , 'price', 'brand', 'reviewLength'
    , 'reviewWords', 'avgWordLength'
    , 'expresiveness', 'ratingDelta'
    , 'priceDelta'], inplace=True)
# Rename index and munge to comply with Azure Text Analytics API
docstoindex.index.rename('id', inplace=True)
docstoindex.rename(columns={'reviewText': 'text'}
                   , inplace=True)
docstoindex['language'] = 'en'
# Prepare to export to json
docstoindex.reset_index(inplace=True)
docstoindex['id'] = docstoindex['id'].astype('str')

docstoindex = docstoindex[['language', 'id', 'text']]

d = {'documents': docstoindex.to_dict(orient='records')}
# print(json.dumps(d, indent=2))


print('Please wait a moment for the results to appear.\n')

# result = GetSentiment (js)
result = GetSentiment(d)
# print(json.dumps(json.loads(result), indent=4))


# Bring JSON into pandas dataframe
from pandas.io.json import json_normalize
datajson = json.loads(result)
datajson = json_normalize(datajson['documents'])

# Save to csv for tomorrow
datajson.to_csv('/Users/pacoc/data_out/dataframeSentiment_2ndround.csv')

# Merge with reviews and save
sentiment = pd.Series(datajson['score'])
reviews = pd.read_csv('/Users/pacoc/data_out/auto_sample_1000_nostrcast.csv')
reviews['sentiment'] = sentiment
reviews.to_csv('/Users/pacoc/data_out/reviews_with_sentiment_ready_2ndround.csv')
