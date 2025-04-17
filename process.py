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




# LOCAL GIT (MANUALLY MANAGED)

    # ids = []
    # processed = []

    # def parse(input):
    #     print("Processing chunk...")
    #     temp = re.split(r'(\s+)', input) 
    #     thisString = ""
    #     thisId = ""
    #     for i in range(len(temp)):
    #         print(f"Processing token {i+1}/{len(temp)}")
    #         if re.search(r'-', temp[i]):  
    #             if len(thisString.strip()) > 5: 
    #                 thisString = re.sub(r"@\w+|#\w+", "", thisString.strip())
    #                 ids.append(thisId)
    #                 processed.append(thisString)
    #                 yield thisString
    #             thisId = temp[i]
    #             thisString = ""
    #         else:
    #             thisString += temp[i]
            
    #     if thisString.strip(): 
    #         thisString = re.sub(r"@\w+|#\w+", "", thisString.strip())
    #         ids.append(temp[len(temp)-1])
    #         processed.append(thisString)
    #         yield thisString

    # def process_file(file_path, chunk_size=1024 * 1024): 
    #     with open(file_path, "r", encoding="utf-8") as file:
    #         while True:
    #             chunk = file.read(chunk_size)
    #             if not chunk:
    #                 break
    #             yield from parse(chunk)

    # def contains_chinese(text):
    #     # Regular expression pattern to match Chinese characters
    #     chinese_char_pattern = re.compile(r'[\u4e00-\u9fff]+')
    #     return bool(chinese_char_pattern.search(text))
    
    
# import json
# from transformers import pipeline
# import re
# import torch
# from tqdm import tqdm

# try:
#     # Load models from models.json
#     with open("models.json", "r", encoding="utf-8") as f:
#         models = json.load(f)

#     # Load labels from labels.json
#     with open("labels.json", "r", encoding="utf-8") as f:
#         labels = json.load(f)

#     # Load existing results from out.json if it exists
#     try:
#         with open("out.json", "r", encoding="utf-8") as f:
#             existing_results = json.load(f)
#     except FileNotFoundError:
#         print("No existing results found")
#         existing_results = []

#     # Convert existing results to a dictionary for quick lookup
#     existing_scores = {entry["id"]: entry for entry in existing_results}

#     print("Models loaded")
#     # Create sentiment analysis pipelines for each model
#     classifiers = [pipeline("sentiment-analysis", model=model, device=-1) for model in models]

#     results = []

#     for i in tqdm(range(len(labels))):
#         sentence = labels[i]["contents"]
#         id = labels[i]["id"]
#         mixed = labels[i]["mixed"]

#         # Check if the label has already been processed
#         if id in existing_scores:
#             # Reuse the existing result
#             results.append(existing_scores[id])
#             continue

#         # Process the label if it hasn't been processed yet
#         model_results = {}
#         for classifier, model_name in zip(classifiers, models):
#             result = classifier(sentence)
#             score = result[0]['score']  # Access the score from the first dictionary in the list
#             model_results[model_name] = score

#         # Append the new result
#         results.append({"contents": sentence, "scores": model_results, "mixed": mixed, "id": id})

#     # Write updated results to out.json
#     with open("out.json", "w", encoding="utf-8") as out_file:
#         json.dump(results, out_file, ensure_ascii=False, indent=4)

# except Exception as e:
#     print(f"An error occurred: {e}")
