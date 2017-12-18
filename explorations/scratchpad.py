# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 14:14:36 2017

@author: francruz

"""
# Open the existing index
import whoosh
import whoosh.index as index

# ix = index.open_dir('/Users/pacoc/data_out/indexdir', indexname='automotive')
# ix = index.open_dir('/Users/pacoc/data_out/indexdir', indexname='small_automotive')
# ix = index.open_dir('c:\\Users\\francruz\\data_out\\indexdir', indexname='small_automotive')
ix = index.open_dir('/Users/pacoc/data_out/indexdir', indexname='small_automotive')

from whoosh.qparser import QueryParser

qp = QueryParser("title", schema=ix.schema)
q = qp.parse('start')

searcher = ix.searcher()
searcher.search(q)
results = searcher.search(q)
results[9]

c = searcher.collector(limit=3)
results = searcher.search_with_collector(q, c)

with ix.searcher() as s:
   results = s.search(q)

   for line in results:
       print(line['title'])
# if __name__ == "__main__":


# Section for dictionary creation
import pandas as pd
import csv
docstoindex = pd.read_csv('/Users/pacoc/data_out/subsetAuto.csv', dtype='str')


docstoindex['reviewText'].to_json(orient = 'index')


# Load the dataframe from csv
import pandas as pd
import json
docstoindex = pd.read_csv('/Users/pacoc/data_out/subsetAuto.csv', dtype='str')
# Drop column not needed for sentiment analysis
docstoindex.drop(columns=['asin', 'helpful', 'overall'
                          , 'reviewTime', 'title'
                          , 'price', 'brand', 'reviewLength'
                          , 'reviewWords', 'avgWordLength'
                          , 'expresiveness', 'ratingDelta'
                          , 'priceDelta'], inplace=True)
# Rename index and munge to comply with Azure Text Analytics API
docstoindex.index.rename('id', inplace = True)
docstoindex.rename(columns = {'reviewText':'text'}
                   , inplace=True)
docstoindex['language'] = 'en'
# Prepare to export to json
d = {'documents':docstoindex.reset_index().to_dict(orient = 'records')}
# Dump for json, format ready for API
js = json.dumps(d, indent = 2)




a = list(tempcsv['helpful'].values)
useful_res = []
for val in a:
    val_a,val_b = val.split(',')
    r = re.compile(r'[{}]'.format(punctuation))
    a_r = r.sub('', val_a).strip()
    b_r = r.sub('', val_b).strip()
    if b_r != '0':
        useful_res.append(int(a_r)/int(b_r))
    else:
        useful_res.append(None)
usefulness = pd.Series(useful_res)