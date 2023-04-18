import os
import re
import pandas as pd
import numpy as np
from model import *
#text preprocessing
import re
import nltk
nltk.download('omw-1.4')
from nltk.stem.porter import PorterStemmer
nltk.download('wordnet') 
from nltk.stem.wordnet import WordNetLemmatizer
import pickle
from deep_translator import GoogleTranslator
from rank_bm25 import BM25Okapi
import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
import configparser


def translation(query,language):
    translated = GoogleTranslator(source='auto', target=language).translate(query)
    return translated

def preprocess(text): 
    stop_words = {'about', 'after', 'own', 'hers', 'them', "didn't", "it's", 'few', 'but', 'too', 'ma', 'do', 'against', 'yourself', 'again', 'how', 'mustn', 'myself', 'your', 'does', 'when', 'through', 'it', 'didn', 're', 'down', 'until', 's', 'doesn', 'did', 'ourselves', 'haven', 'in', "wouldn't", 'ours', 'not', 't', 'had', 'she', 'why', 'these', 'whom', 'of', 'wouldn', 'he', 'they', 'each', 'll', "isn't", "needn't", 'yours', 'up', 'their', 'be', 'to', 'who', 'aren', 'and', 'where', "doesn't", 'for', "hasn't", "shouldn't", 'can', 'o', 'me', "aren't", 'under', "shan't", 'we', 'yourselves', 'our', 'themselves', 'what', 'doing', "you've", 'his', 'the', 'd', 'you', 'so', "couldn't", 'both', 'no', 'most', "she's", 'below', 'same', 'was', "weren't", 'itself', 'theirs', 'before', 'some', 'him', 'over', 'don', 'now', 'were', 'couldn', 'there', "wasn't", 'off', 'above', 'is', 'other', 'while', 'as', 'further', 'm', 'have', 'during', 'herself', 'on', 'weren', 'should', 'y', 'ain', 'won', "haven't", "you're", "you'll", 'shouldn', 'from', 'more', 'such', 'just', 'himself', 've', 'then', "hadn't", 'her', "mightn't", 'wasn', 'mightn', 'if', 'out', "won't", 'shan', 'will', 'isn', 'very', 'i', 'a', 'because', 'has', 'only', 'by', 'an', 'am', 'being', "should've", 'once', 'this', 'hadn', "that'll", 'my', 'into', 'with', 'between', 'are', 'those', 'nor', 'all', 'which', 'here', "don't", 'or', "mustn't", 'hasn', 'needn', 'any', 'that', 'its', 'having', 'than', 'been', "you'd", 'at'}
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

def bm25(articles, df_dic, title_w, abstract_w, query):
    corpus_title = []
    corpus_abstract = []
    
    for article in articles:
        arr = df_dic.iloc[article].to_numpy()
        #title
        if type(arr[1]) != float:
            preprocessedTitle = preprocess(arr[1])
            corpus_title.append(preprocessedTitle)
        else:
            corpus_title.append(" ")
        
        #abstract
        if type(arr[2]) != float:
            preprocessedAbst = preprocess(arr[2])
            corpus_abstract.append(preprocessedAbst)
        else:
            corpus_abstract.append(" ")
            
    query = preprocess(query)
    
    tokenized_query = query.split(" ")
    
    tokenized_corpus_title = [doc.split(" ") for doc in corpus_title]
    tokenized_corpus_abstract = [doc.split(" ") for doc in corpus_abstract]
    
    #running bm25 on titles
    bm25_title = BM25Okapi(tokenized_corpus_title)
    doc_scores_titles = bm25_title.get_scores(tokenized_query)
    #weighting array
    doc_scores_titles = np.array(doc_scores_titles)
    doc_scores_titles = doc_scores_titles**title_w
    
    #running bm25 on abstracts
    bm25_abstract = BM25Okapi(tokenized_corpus_abstract)
    doc_scores_abstracts = bm25_abstract.get_scores(tokenized_query)
    #weighting
    doc_scores_abstracts = np.array(doc_scores_abstracts)
    doc_scores_abstracts = doc_scores_abstracts ** abstract_w
    
    #summing up the two different scores
    doc_scores = np.add(doc_scores_abstracts,doc_scores_titles)
    
    #creating a dictionary with the scores
    score_dict = dict(zip(articles, doc_scores))
    
    #creating list of ranked documents high to low
    doc_ranking = sorted(score_dict, key=score_dict.get, reverse = True)
    
    #get top 100
    doc_ranking = doc_ranking[0:10]
    
    """for i in range(len(doc_ranking)):
        dic_entry = df_dic.get(doc_ranking[i])
        doc_ranking[i] = dic_entry[0]"""
    
    return doc_ranking

def getPotentialArticleSubset(query):
    #load in inverted indices
    invertedIndices = pickle.load(open("invertedIndices_FINAL.p", "rb"))
    
    #preprocess query and split into individual terms
    query = preprocess(query)
    queryTerms = query.split(' ')
    
    potentialArticles = []
    #concatenate list of potential articles by looping through potential articles for each word in query
    for word in queryTerms:
        if word in invertedIndices: #so if someone types in nonsensical query term that's not in invertedIndices, still won't break!
            someArticles = invertedIndices[word]
            potentialArticles = potentialArticles + someArticles
            
    #convert to set then back to list so there are no repeat articles
    potentialArticles = list(set(potentialArticles))
    return potentialArticles

def retrieve(queries):
    #performing information retrieval
    
    df_dic = pd.read_csv("data_withKeywords.csv")
    results = []
    ans=[]
    for q in queries:
        tmp = getBestAnswer(q,list(df_dic['question']))
        articles = getPotentialArticleSubset(q)
        result = bm25(articles,df_dic,1,2,q)
        print(tmp)
        for p in tmp:
            if p not in result:
                result.append(p)
        print(result)
        results.append(result)
    #Output results
    for query in range(len(results)):
        for rank in range(len(results[query])):

            text=df_dic["answer"][results[query][rank]]
            question=queries[query]
            question_answerer = AnswerBert(question,text)
            ans.append([question_answerer[1],question_answerer[0],str(results[query][rank])])
    ans=sorted(ans,key=lambda x:x[0], reverse=True)
    return ans

def result(query):
    config = configparser.ConfigParser()
    config.read('variables.ini')
    LANG=config['VARIABLES']['LANG']
    LANG=LANG.replace('"','')
    print(LANG)
    query = translation(query,'en')
    res = retrieve([query])
    print('done')
    l=0
    while(res[l][1]==''):
        l+=1
    
    if res != None and res[l][0]>0.1:
        ans = translation(res[l][1],LANG)
        '''print(res[l][1])
        ind=res[l][2]
        det=df_dic['answer'][int(ind)]
        print(det)'''
        DETAILS = int(res[l][2])
        BOOL=1
        print(DETAILS,BOOL)
        config.set('VARIABLES', 'DETAILS',str(DETAILS))
        config.set('VARIABLES', 'BOOL',str(BOOL))
        with open('variables.ini', 'w') as configfile:
            config.write(configfile)
        print(ans)
        return ans
    else:
        rep='Sorry, Cannot answer this question'
        BOOL=0
        print(BOOL)
        config.set('VARIABLES', 'BOOL',str(BOOL))
        with open('variables.ini', 'w') as configfile:
            config.write(configfile)
        rep = translation(rep,LANG)
        return rep
def more_details():
    config = configparser.ConfigParser()
    config.read('variables.ini')
    LANG=config['VARIABLES']['LANG']
    LANG=LANG.replace('"','')
    DETAILS=config['VARIABLES']['DETAILS']
    print(DETAILS)
    df_dic = pd.read_csv("data_withKeywords.csv")
    try:
        txt=df_dic['answer'][int(DETAILS)][0:4096]
        txt=txt.split('.')
        tmp=txt.pop()
        txt = ".".join(txt) 
        print(txt)
        res= translation(str(txt),LANG)
        return res
    except:
        return "Error while fetching"
    

