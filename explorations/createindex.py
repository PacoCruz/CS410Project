# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 14:14:36 2017

@author: francruz

"""
import pandas as pd
import whoosh
import csv


# Creating the schema
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import StemmingAnalyzer
schema = Schema(asin = KEYWORD(stored=True,scorable=True,sortable=True),
                helpful = STORED,
                reviewText = TEXT(analyzer=StemmingAnalyzer(), phrase=False, stored=True),
                overall = TEXT(analyzer=StemmingAnalyzer(), phrase=False),
                reviewTime = ID(stored=True),
                title = TEXT(analyzer=StemmingAnalyzer(), phrase=False, stored=True),
                price = STORED,
                brand = KEYWORD(stored=True),
                reviewLength = STORED,
                reviewWords = STORED,
                avgWordLength = STORED,
                expresiveness = STORED,
                ratingDelta = STORED,
                priceDelta = STORED)


# Creating the index
from whoosh import index
import os, os.path

if not os.path.exists("/Users/pacoc/data_out/indexdir"):
    os.mkdir("/Users/pacoc/data_out/indexdir")

# ix = index.create_in("/Users/pacoc/data_out/indexdir", schema, indexname="automotive")
# ix = index.create_in("/Users/pacoc/data_out/indexdir", schema, indexname="small_automotive")
ix = index.create_in("/Users/pacoc/data_out/indexdir", schema, indexname="small_automotive")

# Indexing Documents
# docstoindex = pd.read_csv('/Users/pacoc/data_out/automotive.csv', dtype='str') <--- All reviews
# docstoindex = pd.read_csv('/Users/pacoc/data_out/subsetAuto.csv', dtype='str') <--- Just subset
docstoindex = pd.read_csv('/Users/pacoc/data_out/subsetAuto.csv', dtype='str')
writer = ix.writer()
for row in docstoindex.itertuples(name=None, index=False):
    v_asin, v_helpful, v_reviewText, v_overall, v_reviewTime, v_title\
        , v_price, v_brand, v_reviewLength, v_reviewWords\
        , v_avgWordLength, v_expresiveness, v_ratingDelta, v_priceDelta = row

    writer.add_document(asin = str(v_asin), helpful = str(v_helpful), overall = str(v_overall),
                        reviewTime = str(v_reviewTime), title = str(v_title), price = str(v_price),
                        brand = str(v_brand), reviewLength = str(v_reviewLength),
                        reviewWords = str(v_reviewWords), avgWordLength = str(v_avgWordLength),
                        expresiveness = str(v_expresiveness), ratingDelta = str(v_ratingDelta),
                        priceDelta = str(v_priceDelta), reviewText = str(v_reviewText))

 #   writer.add_document(asin = v_asin, helpful = v_helpful, overall = v_overall,
 #                       reviewTime = v_reviewTime, title = v_title, price = v_price,
 #                       brand = v_brand, reviewLength = v_reviewLength,
 #                       reviewWords = v_reviewWords, avgWordLength = v_avgWordLength,
 #                       expresiveness = v_expresiveness, ratingDelta = v_ratingDelta,
 #                       priceDelta = v_priceDelta, reviewText = v_reviewText)
writer.commit()



# if __name__ == "__main__":
