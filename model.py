import torch
from torch.nn.functional import softmax
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import re 
import pandas as pd
from fse import SplitIndexedList
from fse.models import uSIF
import gensim
import gensim.downloader as api
from nltk.corpus import stopwords
from sklearn import metrics
from sklearn.metrics.pairwise import cosine_similarity


tokenizer = AutoTokenizer.from_pretrained('juliusco/biobert-base-cased-v1.1-squad-finetuned-covdrobert')
model = AutoModelForQuestionAnswering.from_pretrained('juliusco/biobert-base-cased-v1.1-squad-finetuned-covdrobert')

from fse.models import uSIF
glove = api.load("glove-wiki-gigaword-100")
model_sif = uSIF(glove, workers=2, lang_freq="en")
df = pd.read_csv('data_withKeywords.csv')
df = df.dropna(subset=['question'])
df = df.dropna(subset=['answer'])
df['answer'] = df['answer'].apply(lambda x: re.sub(r'(\n)+', '. ', x))
df = df.drop(['index', 'keywords'], axis='columns')
def cleanQuestion(text):
  text = str(text)
  text = text.lower()
  words = re.sub(r'[^\w\s]', '', text).split()
  return " ".join([word for word in words])

def cleanAnswer(text):
  text = str(text)
  text = text.lower()
  words = re.sub(r'[^\w\s]', '', text).split()
  return " ".join([word for word in words])

def getSim(q, x):
  x = (str(x).split(), 0)
  sim = metrics.pairwise.cosine_similarity(model_sif.infer([q]), model_sif.infer([x]))
  return sim

def getAnswer(question, context):
  q = (str(question).split(), 0)
  c = pd.DataFrame(str(context).split('.'))
  c['sim'] = c[0].apply(lambda x: getSim(q, x))
  max = c.sort_values(by='sim', ascending=False).iloc[:3]
  return max

def getBestAnswer(question, potentials):
  q = (str(question).split(), 0)
  c = pd.DataFrame(potentials)
  c['sim'] = c[0].apply(lambda x: getSim(q, x))
  max = c.sort_values(by='sim', ascending=False).iloc[:5]
  ind=list(max.index.tolist())
  return ind

df['question'] = df['question'].apply(lambda x: cleanQuestion(x))
df['answer'] = df['answer'].apply(lambda x: cleanAnswer(x))
allQuestion = '. '.join(list(df['question']))
allAnswer = '. '.join(list(df['answer']))
text = allQuestion + allAnswer
s = SplitIndexedList(text.split('.'))
model_sif.train(s)
def get_split(text1):
  
  l_total = []
  l_parcial = []
  if len(text1.split())//150 >0:
    n = len(text1.split())//150
  else: 
    n = 1
  for w in range(n):
    if w == 0:
      l_parcial = text1.split()[:250]
      l_total.append(" ".join(l_parcial))
    else:
      l_parcial = text1.split()[w*150:w*150 + 250]
      l_total.append(" ".join(l_parcial))
  return l_total
     

def AnswerBert(question, context):

  
  context_list = get_split(context)

  ans = []

  for c in context_list:

    inputs = tokenizer(question, c, add_special_tokens=True, return_tensors="pt")
    outputs = model(**inputs)

    non_answer_tokens = [x if x in [0,1] else 0 for x in inputs.sequence_ids()]
    non_answer_tokens = torch.tensor(non_answer_tokens, dtype=torch.bool)
    
    potential_start = torch.where(non_answer_tokens, outputs.start_logits, torch.tensor(float('-inf'),dtype=torch.float))
    potential_end = torch.where(non_answer_tokens, outputs.end_logits, torch.tensor(float('-inf'),dtype=torch.float))

    potential_start = softmax(potential_start, dim = 1)
    potential_end = softmax(potential_end, dim = 1)
    
    answer_start = torch.argmax(potential_start)
    answer_end = torch.argmax(potential_end)
    answer = tokenizer.decode(inputs.input_ids.squeeze()[answer_start:answer_end+1])
    confidence=potential_start.squeeze()[answer_start] *potential_end.squeeze()[answer_end]
    confidence=confidence.tolist()
 


    ans.append([answer,confidence])

  potentials = []
  ans=sorted(ans,key=lambda x:x[0], reverse=True)
  for i in ans:
    if ('SEP' not in i[0]) and ('CLS' not in i[0]):
      potentials.append([re.sub('(#)+', '', i[0]),i[1]])

  answer=sorted(potentials,key=lambda x:x[1], reverse=True)

  print (answer)


  return answer[0]
     
