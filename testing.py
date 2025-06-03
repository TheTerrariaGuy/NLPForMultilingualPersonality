import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline

classifier5 = pipeline(
    model="lxyuan/distilbert-base-multilingual-cased-sentiments-student", 
    return_all_scores=True
)
def model5Results(sentence):
    classifier5("i love this!")[0][0]['label']
