# Exploring the Relationship Between Reviews Sentiment and Length, Price in Amazon Reviews
## Introduction
This project started to fulfill the Technology Project requirement of the **CS410: Text Information Systems** course at the University of Illinois - Urbana-Champaign. I expect to continue its development as I progress in my Master in CS and apply concepts and knowledge from other disciplines.

With support from my TA Ismini Lourentzou, I decided to explore the relationship between the sentiment inferred on reviews by Amazon users and the price of the goods purchased, under the hypothesis that review length and their tone are predictors of product price. It is a very naïve expectation based on the hypothesis that a high price would command a longer explanation, and that higher prices generally bring more positive reviews.

To explore this hypothesis, I used the [datasets](http://jmcauley.ucsd.edu/data/amazon/) made available by [Julian McAuley](julian.mcauley@gmail.com). The website above provides a detailed explanation of the data schema and how to parse the files for use in applications. Since the files are quite large, for the purpose of this course I will make them temporarily available in a [publicly available share](https://uofi.box.com/s/lmutpr56zevns6q4tx9rl1r4dr3t9o3k) for replicating and grading my work.
## Datasets Description
The data I am using are split into two files:

- Product Review

```
{
"reviewerID": "A2SUAM1J3GNN3B",
"asin": "0000013714",
"reviewerName": "J. McDonald",
"helpful": [2, 3],
"reviewText": "I bought this for my husband... Great purchase though!",
"overall": 5.0,
"summary": "Heavenly Highway Hymns",
"unixReviewTime": 1252800000,
"reviewTime": "09 13, 2009"
}
```

For our purpose, we will only use the `asin` as a key to join with the metadata information, and sentiment and text relevant fields, `helpful`, `reviewText`, and `overall`.

- Review Metadata

```
{
  "asin": "0000031852",
  "title": "Girls Ballet Tutu Zebra Hot Pink",
  "price": 3.17,
  "imUrl": "http://ecx.images-amazon.com/images/...",
  "related":
  {
	  "also_bought": ["B00JHONN1S", "B002BZX8Z6",..., "B00BFXLZ8M"],
	  "bought_together": ["B002BZX8Z6"]
  },
  "salesRank": {"Toys & Games": 211836},
  "brand": "Coxlures",
  "categories": [["Sports & Outdoors", "Other Sports", "Dance"]]
}
```

Again, we only need `asin` for our join, and `price`.

## Work Description
At its current stage, the project main artifact is the Python 3 script `amznreviews.py`. The key requirements are the Pandas package for data manipulation and the NLTK package for sentiment analysis. I am also including additional scripts related but not relevant for this project that were used in initial stages of the project to explore indexing concepts (with the `whoosh` package) and to use the Microsoft Azure Text Analytics REST API for sentiment analysis.

To comply with the project requirements, this script can be used with any of the files provided in the website of reference and the dataset I provide. By default, it uses the smallest of these dataset pairs (`meta_Musical_Instruments.json.gz`and `reviews_Musical_Instruments.json.gz`) but it can be used with any of the dataset pairs available as:
> `python3 amznreviews.py reviewsFile metadataFile`

The only screen output is the correlation matrix for all the original numerical features in the joined dataset plus the additional features that I will describe below. Other artifacts are placed in the `data_out` directory as follows:

- `all_features_with_sentiment_merge.csv` file, that can be used for further analysis in R or re-imported in Python for additional exploration. I used this file to prepare in R a more attractive visual than the one generated by the Python script, and stored as `corrplot.png`.
- `corrplot.png` is a Seaborn generated heat map of the correlation metric to visually inspect the relationship between the features of interest.

A second artifact, the R script `corplot.R` was written for the simple purpose of beautifying the output of the Python script to generate a more insightful visual of the correlations between the features. When executed, it takes the output of the Python script and produces two plots:

- `corplotR.png` is a correlogram that simultaneously represents the correlations strength and values for all pairwise combinations of features.
- `corplotValuesR.png` is a simpler correlation representation that only shows the correlation values.

## Features
The datasets will need to be preprocessed before any analysis is done to ensure that the data conform to the schema needed to apply the sentiment analysis. Additionally, new features will be added to explore the relationships between price, rating, usefulness, and text content of the reviews. This is a description of the added features:
- `reviewLength`: calculated as the number of characters in the product review.
- `reviewWords`: calculated as the number of words in the product review. It is implemented as a regular expression pattern match. Unfortunately, the decision to use NLTK came the the project was already under way, but it might have been more efficient to use the provided word tokenizer.
- `avgWordLength`: calculated as the quotient of `reviewWLength` divided by `reviewWords`. It was intended to provide a measurement of sophistication in expression (e.g.: using longer words).
- `expressiveness`: calculated as the ratio of number of words in a review divided by the average length in word of all reviews. Also intended as a normalization of review length relative to other reviewers.
- `ratingDelta` and `priceDelta` are like `expresiveness` a normalization of rating and price relative to their respective averages.
- `usefulness`: since the `helpful` field as available is a pair of values indicating how many of the review viewers have voted it as useful, it needs to be transformed into a numerical feature. It is represented as the ratio of reviews rated as helpful to the total of rated reviews by the community.

## Exploration
The scope and output of this report is limited by time constraints and most importantly, my learning the use of the tools required as I was building the project. Not having a Computer Science background meant having to learn `Pandas` for data wrangling, `NLTK` for sentiment analysis, JSON manipulation for conforming the output to the expected input by the Azure Sentiment Analysis API, `whoosh` for indexing and searching a corpus, and in general commonplace practices in Data Exploration that I was unfamiliar with.

Under these constraints, most of the effort was applied to building the dataset and applying the sentiment analysis to the reviews texts.

### The Results
The following visualization provides a quick view of the result of this exploration.
![Correlogram of Amazon Reviews Features](data_out/corplotR.png?raw=True "Correlogram of Amazon Reviews Features")

I used the Pearson Correlation coefficient to indicate the relationship between pairs of features, given as in the following equation:

![Pearson Correlation](explorations/Pearson.png?raw=True "Pearson Correlation")

There is no strong correlation between any pair of features in our sentiment annotated dataset. This result doesn't support the initial hypothesis of an underlying relationship between text reviews sentiment and length of the review or product price. The strongest correlation values are summarized below:

 X| sentiment | usefulness | ratingDelta | expressiveness | priceDelta 
 -|------------|-----------|--------------|---------------|------------
sentiment | 1 | 0 | 0.48 | 0.15 | 0 
usefulness | 0 | 1 | 0 | 0.27 | 0.13 
ratingDelta | 0.48 | 0 | 1 | 0 | 0 
expressiveness | 0.15 | 0.27 | 0 | 1 | 0.16 
priceDelta | 0 | 0.13 | 0 | 0.16 | 1 

Considering the statistical criteria used on classifying correlations, all these results fall under the category of 'Weak' (0.2 - 0.4) or 'Extremely Weak' (0 - 0.2), except for the relationship between `sentiment` and `ratingDelta` which is considered 'Medium' at 0.48 (and by extension, to any feature related to `helpfulness` from which is derived).

After this result - which came consistently over the `Musical Instruments`, `Automotive`, and `Food` categories - it became clear that the original hypothesis was not sustained, and that there is no discernible relationship between the features part of my original hypothesis.
## Further Research
The fact that the only evidence of higher than weak correlation between a pair of features is found between `sentiment` and `ratingDelta`, is representative of the performance of the sentiment classifier. Since `ratingDelta` is derived from `overall`, a direct indicator of the satisfaction of the reviewer with the product, it is only natural that there is evidence of relationship between them.

This relationship opens the opportunity to understanding why this relationship is still moderate and might be related to the performance of the Sentiment Analyzer used in this Exploration: `NLTK's VADER`. Interestingly, in one of my initial experimentations I used Azure's Cognitive Services (ACS) API to perform sentiment analysis on a sample of the reviews, and the correlation coefficient for this pair of features was 0.32.

![Pearson Correlation of Sentiment Analysis using Azure Cognitive Services](explorations/corplotRAzure.png?raw=True "Azure Cognitive Services")

The difference itself is no as interesting as the fact that the VADER sentiment analysis uses rules inferred from a finite and reduced number of words to assign a sentiment value, and the ACS use a trained model based on a curated and annotated corpus. That the performance of a statistical/deterministic Analyzer matches that of an ML-trained commercial model indicates either a glaring oversight in my first attempt at using ACS, or the result of a model not flexible enough for this type of text content. I will focus my analysis after this course ends on understanding what are the factors that may be influencing this result.

# Appendix
## Discarded Explorations
### 1. `whoosh` Indexer and Searcher

Per course staff suggestion, I researched the implementation and use of the Python [`whoosh`](https://pypi.python.org/pypi/Whoosh/) package to experiment and familiarize myself with indexing and searching platforms. While I was not able to integrate this component as planned in the original, more ambitious project scope, It helped me experiment and solidify the topics covered in class, specifically the creation of index and postings files, ranking functions, and parsing of queries and documents to provide a set of ranked relevant results. Here is an example that summarizes how to search a previously built index:
```python
# Open the existing index
import whoosh
import whoosh.index as index
ix = index.open_dir('/Users/pacoc/data_out/indexdir', indexname='small_automotive')

from whoosh.qparser import QueryParser

qp = QueryParser("title", schema=ix.schema)
q = qp.parse('start')

with ix.searcher() as s:
   results = s.search(q)

   for line in results:
       print(line['title'])
```
Other areas for of discovery using `whoosh` were the ability of filtering results and applying facets to collapse/group results. I will continue my learning in this area to better apply the topics discovered in class.

### 2. Azure Cognitive Services - Text Sentiment Analysis
Before using `NLTK` I performed some sentiment analysis on samples of the dataset using Microsoft's Azure Cognitive Services API. While I finally decided  not to use it for this project due to being a commercial service with a significant cost for the size of the datasets used in this project, I was able to use its Free Tier offer for practice.

The services include AI services for Vision, Knowledge, Speech, or Language among other options. In particular, for Language includes a Linguistic Analysis API that I didn't explore, and a [Text Analytics](https://azure.microsoft.com/en-us/services/cognitive-services/text-analytics/) API through a REST API, is able to analyze a text and to provide:
- **Sentiment Analysis**: The Sentiment Analysis API evaluates text input and returns a sentiment score for each document, ranging from 0 (negative) to 1 (positive). This capability is useful for detecting positive and negative sentiment in social media, customer reviews, and discussion forums. Models and training data are provided by the service.
- **Key Phrase Extraction**: The Key Phrase Extraction API evaluates unstructured text, and for each JSON document, returns a list of key phrases. This capability is useful to quickly identify the main points in a collection of documents.
- **Language Detection**: The Language Detection API evaluates text input and for each document returns language identifiers with a score indicating the strength of the analysis, recognizing up to 120 languages. The results of this analysis can be parsed to determine which language is used in the input document. The response also returns a score which reflects the confidence of the model (a value between 0 and 1).
Using the Azure Sentiment Analyzer, I was able to annotate with sentiment a set of documents around 100 times faster than using VADER. A representative excerpt of the code I used follows below; it can be easily adapted to read the intermediate files created by the `amznreviews.py` module:

```python
import pandas as pd
import json
import http.client, urllib.request, urllib.parse, urllib.error, base64

# accessKey string value for Azure Text Analytics API.

accessKey = '****************************'

# Azure regional information
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
# Drop columns not supported by the sentiment analysis API
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

print('Please wait a moment for the results to appear.\n')

result = GetSentiment(d)

# Use the following line for debugging, validation.
# print(json.dumps(json.loads(result), indent=4))

# Bring JSON into pandas dataframe
from pandas.io.json import json_normalize
datajson = json.loads(result)
datajson = json_normalize(datajson['documents'])

# Save to csv for later use
datajson.to_csv('/Users/pacoc/data_out/dataframeSentiment_2ndround.csv')
	
# Merge with reviews and save
sentiment = pd.Series(datajson['score'])
reviews = pd.read_csv('/Users/pacoc/data_out/auto_sample_1000_nostrcast.csv')
reviews['sentiment'] = sentiment
reviews.to_csv('/Users/pacoc/data_out/reviews_with_sentiment_ready_2ndround.csv')
```

