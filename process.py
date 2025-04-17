import json
from transformers import pipeline
import re
import torch
from tqdm import tqdm

try:
    # List of models to use
    
    with open("models.json", "r", encoding="utf-8") as f:
        models = json.load(f)
    
    with open("labels.json", "r", encoding="utf-8") as f:
        labels = json.load(f)
    
    print("Models loaded")
    # Create sentiment analysis pipelines for each model
    classifiers = [pipeline("sentiment-analysis", model=model, device=-1) for model in models]

    results = []

    for i in tqdm(range(len(labels))):
        sentence = labels[i]["contents"]
        id = labels[i]["id"]
        mixed = labels[i]["mixed"]
        model_results = {}
        for classifier, model_name in zip(classifiers, models):
            result = classifier(sentence)
            score = result[0]['score']  # Access the score from the first dictionary in the list
            model_results[model_name] = score
        results.append({"contents": sentence, "scores": model_results, "mixed": mixed, "id": id})

    with open("out.json", "w", encoding="utf-8") as out_file:
        json.dump(results, out_file, ensure_ascii=False, indent=4)

except Exception as e:
    print(f"An error occurred: {e}")



