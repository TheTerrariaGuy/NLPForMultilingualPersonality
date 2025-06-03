import json
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import re
import torch
from tqdm import tqdm

# Loading things

with open("labels.json", "r", encoding="utf-8") as f:
    labels = json.load(f)

try:
    with open("out.json", "r", encoding="utf-8") as f:
        currOut = json.load(f)
    print("out.json exists.")
except FileNotFoundError:
    currOut = []
    print("out.json does not exist, creating a new one.")

print("Models loaded")

# ========== Models ==========

model1 = "agentlans/mdeberta-v3-base-sentiment"
model2 = "joeddav/xlm-roberta-large-xnli"
model3 = "tabularisai/multilingual-sentiment-analysis"
model4 = "clapAI/modernBERT-large-multilingual-sentiment"
model5 = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"

# ========== Functions for sentiment for each model ==========


tokenizer1 = AutoTokenizer.from_pretrained(model1)
model1 = AutoModelForSequenceClassification.from_pretrained(model1)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model1 = model1.to(device)
def model1Results(sentence):
    inputs = tokenizer1(sentence, return_tensors="pt", truncation=True, padding=True).to(device)
    with torch.no_grad():
        logits = model1(**inputs).logits.squeeze().cpu()
    return logits.tolist()


tokenizer2 = AutoTokenizer.from_pretrained(model2, use_fast=False)
model2 = AutoModelForSequenceClassification.from_pretrained(model2)
classifier2 = pipeline("zero-shot-classification", model=model2, tokenizer=tokenizer2)
def model2Results(sentence):
    return classifier2(sentence, candidate_labels=labels)


classifier3 = pipeline("text-classification", model=model3)
def model3Results(sentence):
    return classifier3(sentence)


tokenizer4 = AutoTokenizer.from_pretrained(model4)
classifier4 = AutoModelForSequenceClassification.from_pretrained(model4, torch_dtype=torch.float16)
classifier4.to(device)
classifier4.eval()
id2label = classifier4.config.id2label
def model4Results(text):
    inputs = tokenizer4(text, return_tensors="pt").to(device)
    with torch.inference_mode():
        outputs = classifier4(**inputs)
        prediction = outputs.logits.argmax(dim=-1)
    return id2label[prediction.item()]


classifier5 = pipeline(
    model=model5, 
    return_all_scores=True
)
def model5Results(sentence):
    classifier5("i love this!")[0][0]['label']


try:
    for i in tqdm(range(len(labels))):
        if i < len(currOut) and "scores" in currOut[i]: # comment out if repairing
            continue
        sentence = labels[i]["contents"]
        id = labels[i]["id"]
        mixed = labels[i]["mixed"]
        model_results = {}
        model_results[model1] = model1Results(sentence)
        model_results[model2] = model2Results(sentence)
        model_results[model3] = model3Results(sentence)
        model_results[model4] = model4Results(sentence)
        model_results[model5] = model5Results(sentence)
        currOut.append({"contents": sentence, "scores": model_results, "mixed": mixed, "id": id})
finally:
    with open("out.json", "w", encoding="utf-8") as out_file:
        json.dump(currOut, out_file, ensure_ascii=False, indent=4)




