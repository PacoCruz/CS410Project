# Get data
# install.packages('corrplot')
library(corrplot)
library(readr)
datawork <- read_csv("./data_out/all_features_with_sentiment_merge.csv", 
                     col_types = cols(asin = col_skip(), avgWordLength = col_skip(), 
                                      expresiveness = col_double(), helpful = col_skip(), 
                                      overall = col_double(), price = col_double(), 
                                      priceDelta = col_double(), ratingDelta = col_double(), 
                                      reviewLength = col_double(), reviewText = col_skip(), 
                                      reviewWords = col_double(), sentiment = col_double(), 
                                      usefulness = col_double()))
png('./data_out/corplotR.png')
corrplot.mixed(cor(datawork))
dev.off()
png('./data_out/corplotValuesR.png')
corrplot(cor(datawork), method = 'number')
dev.off()