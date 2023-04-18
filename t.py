import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os



import re, os, string
import pandas as pd

import re
import nltk
nltk.download('stopwords')
nltk.download('omw-1.4')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
nltk.download('wordnet') 
from nltk.stem.wordnet import WordNetLemmatizer
import pickle


from sklearn.feature_extraction.text import TfidfVectorizer
def preprocess(text): 
    stop_words = set(stopwords.words("english"))
    #Remove punctuations
    text = re.sub('[^a-zA-Z]', ' ', str(text))
    text = text.lower()
    #remove tags
    text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)
    # remove special characters and digits
    text=re.sub("(\\d|\\W)+"," ",text)
    text = text.split()
    ##Stemming
    ps=PorterStemmer()
    text = [ps.stem(word) for word in text if not word in stop_words]
    #Lemmatisation
    lem = WordNetLemmatizer()
    text = [lem.lemmatize(word) for word in text if not word in  stop_words] 
    text = " ".join(text) 
    
    return text

df = pd.read_csv('data.csv')
df=df[['question','answer']].copy()
df.insert(0,"index",0)
df.insert(3, "keywords", "covid19")
text = df['question']+" "+df['answer']
cnt=len(text)
for i in range(cnt):
    text[i] = preprocess(text[i])


print(cnt)

# initialize tf-idf vectorizer
tfidf = TfidfVectorizer()

# fit and transform the corpus
tfidf_matrix = tfidf.fit_transform(text)

# get the feature names (keywords)
feature_names = tfidf.get_feature_names_out()

# iterate through each document and extract the top keywords
for i in range(len(text)):
    print(f"Document {i+1}:")
    scores = {feature_names[j]: tfidf_matrix[i, j] for j in range(tfidf_matrix.shape[1])}
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    print(sorted_scores[:30])
    kew=[]
    for keyword, score in sorted_scores[:30]:
        kew.append(keyword)
    df["index"][i]=i
    df["keywords"][i]=list(set(kew))
def createInvertedIndices(df):
    numEntries = df.shape[0]
    invertInd = {}
    
    for i in range (numEntries):
        entry = df.iloc[i]
        cord_uid = entry['index']       
        keywords = entry['keywords']
        for k in keywords:
            if k not in invertInd:
                invertInd[k] = []
                invertInd[k].append(cord_uid)
            else:
                invertInd[k].append(cord_uid)
    return invertInd
print(df.head(20))
df.to_csv('data_withKeywords.csv')
invertedIndices = createInvertedIndices(df)
pickle.dump( invertedIndices, open( "invertedIndices_FINAL.p", "wb" ) )
