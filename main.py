import json
from transformers import pipeline
import re
import torch

def parse(input):
    temp = re.split(r'(\s+)', input)  # Split by spaces while keeping the spaces
    thisString = ""
    for i in range(len(temp)):
        thisString += temp[i]
        if re.search(r'[.!?]', temp[i]):  # Check for sentence-ending punctuation
            if len(thisString.strip()) > 5: # Check if the sentence is not too short (>4 characters, may chancge)
                thisString = re.sub(r"@\w+|#\w+", "", thisString.strip())
                yield thisString
            thisString = ""
    if thisString.strip():  # Add any remaining text as a sentence
        thisString = re.sub(r"@\w+|#\w+", "", thisString.strip())
        yield thisString

def process_file(file_path, chunk_size=1024 * 1024):  # 1MB chunks
    with open(file_path, "r", encoding="utf-8") as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            yield from parse(chunk)

# creates the sentiment analysis pipeline
classifier = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment", device=-1)
# classifier = pipeline("sentiment-analysis", model="tabularisai/multilingual-sentiment-analysis", device=-1)

# file_path = "inputTest.txt"
file_path = "input.txt"

results = []

for sentence in process_file(file_path):
    result = classifier(sentence)
    score = result[0]['score']  # Access the score from the first dictionary in the list
    results.append({"contents": sentence, "score": score})

with open("out.json", "w", encoding="utf-8") as out_file:
    json.dump(results, out_file, ensure_ascii=False, indent=4)