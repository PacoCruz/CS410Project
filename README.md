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

This relationship opens the opportunity to understanding why this relationship is still moderate and might be related to the performance of the Sentiment Analyzer used in this Exploration: `NLTK's VADER`. Interestingly, in one of my initial experimentations I used Azure's Cognitive Services API to perform sentiment analysis on a sample of the reviews, and the    correlation coefficient for this pair of features was 0.32.

![Pearson Correlation of Sentiment Analysis using Azure Cognitive Services](explorations/corplotRAzure.png?raw=True "Azure Cognitive Services")















# Appendix
## 1. Discarded Explorations.
