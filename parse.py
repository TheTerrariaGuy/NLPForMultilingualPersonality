import json
import re
from tqdm import tqdm

try:
    ids = []
    processed = []

    def parse(input):
        # print("Processing chunk...")
        temp = re.split(r'(\s+)', input)  # Split by spaces while keeping the spaces
        thisString = ""
        thisId = ""
        for i in tqdm(range(len(temp))):
            # print(f"Processing token {i+1}/{len(temp)}")
            if re.search(r'-', temp[i]) and len(temp[i]) > 12:  # Check for new line
                if len(thisString.strip()) > 5:  # Check if the sentence is not too short (>4 characters, may change)
                    thisString = re.sub(r"@\w+|#\w+", "", thisString.strip())
                    ids.append(thisId)
                    processed.append(thisString)
                    yield thisString
                thisId = temp[i]
                thisString = ""
            else:
                thisString += temp[i]
            
        if thisString.strip():  # Add any remaining text as a sentence
            thisString = re.sub(r"@\w+|#\w+", "", thisString.strip())
            ids.append(temp[len(temp)-1])
            processed.append(thisString)
            yield thisString

    def process_file(file_path, chunk_size=1024 * 1024):  # 1MB chunks
        with open(file_path, "r", encoding="utf-8") as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                yield from parse(chunk)

    def contains_chinese(text):
        # Regular expression pattern to match Chinese characters
        chinese_char_pattern = re.compile(r'[\u4e00-\u9fff]+')
        return bool(chinese_char_pattern.search(text))
    
    def contains_english(text):
        # Regular expression pattern to match English characters
        english_char_pattern = re.compile(r'[a-zA-Z]')
        return bool(english_char_pattern.search(text))
    
    
    input_file_path = [
        "data/text_eng.txt",
        "data/text_man.txt"
    ]
    # input_file_path = "input.txt"
    for file_path in input_file_path:
        for sentence in process_file(file_path):
            sentence = sentence
    
    out_file = "labels.json"
    results = []
    
    for i in tqdm(range(len(processed))):
        sentence = processed[i]
        id = ids[i]
        cn = contains_chinese(sentence)
        en = contains_english(sentence)
        
        # mixed: 0 - only English, 1 - only Chinese, 2 - mixed
        if cn and en:
            mixed = 2
        elif cn:
            mixed = 1
        else:
            mixed = 0
        
        results.append({"contents": sentence, "mixed": mixed, "id": id})
    
    with open(out_file, "w", encoding="utf-8") as out_file:
        json.dump(results, out_file, ensure_ascii=False, indent=4)
except Exception as e:
    print(e)
    


# LOCAL GIT (MANUALLY MANAGED)


#     # List of models to use
    # models = [
    #     "nlptown/bert-base-multilingual-uncased-sentiment",
    #     "tabularisai/multilingual-sentiment-analysis",
    #     "issai/rembert-sentiment-analysis-polarity-classification-kazakh",
    #     # "cardiffnlp/twitter-xlm-roberta-base-sentiment-multilingual",
    #     "lxyuan/distilbert-base-multilingual-cased-sentiments-student",
    #     "uer/roberta-base-finetuned-chinanews-chinese",
    #     "uer/roberta-base-finetuned-dianping-chinese"
    # ]

#     # Create sentiment analysis pipelines for each model
#     classifiers = [pipeline("sentiment-analysis", model=model, device=-1) for model in models]

#     file_path = "inputTest.txt"
#     # file_path = "input.txt"

#     results = []

#     # Populate the processed list by iterating over the generator
    # for sentence in process_file(file_path):
    #     print(f"Processed sentence: {sentence}")

#     for i in tqdm(range(len(processed))):
#         sentence = processed[i]
#         id = ids[i]
#         model_results = {}
#         for classifier, model_name in zip(classifiers, models):
#             result = classifier(sentence)
#             score = result[0]['score']  # Access the score from the first dictionary in the list
#             model_results[model_name] = score
#         mixed = contains_chinese(sentence)
#         results.append({"contents": sentence, "scores": model_results, "mixed": mixed, "id": id})

#     with open("out.json", "w", encoding="utf-8") as out_file:
#         json.dump(results, out_file, ensure_ascii=False, indent=4)

#     # Print the lengths of the ids and processed lists
#     print(f"Length of ids: {len(ids)}")
#     print(f"Length of processed: {len(processed)}")

# except Exception as e:
#     print(f"An error occurred: {e}")
    
    






# import json
# from transformers import pipeline
# import re
# import torch
# import os
# # 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
# try:
#     ids = []
#     processed = []
#     def parse(input):
#         print("Processing chunk...")
#         temp = re.split(r'(\s+)', input)  # Split by spaces while keeping the spaces
#         thisString = ""
#         thisId = ""
#         for i in range(len(temp)):
#             print(f"Processing token {i+1}/{len(temp)}")
#             if re.search(r'-', temp[i]):  # Check for new line
#                 if len(thisString.strip()) > 5:  # Check if the sentence is not too short (>4 characters, may change)
#                     thisString = re.sub(r"@\w+|#\w+", "", thisString.strip())
#                     ids.append(thisId)
#                     processed.append(thisString)
#                     yield thisString
#                 thisId = temp[i]
#                 thisString = ""
#             else:
#                 thisString += temp[i]
            
#         if thisString.strip():  # Add any remaining text as a sentence
#             thisString = re.sub(r"@\w+|#\w+", "", thisString.strip())
#             ids.append(temp[len(temp)-1])
#             processed.append(thisString)
#             yield thisString

#     def process_file(file_path, chunk_size=1024 * 1024):  # 1MB chunks
#         with open(file_path, "r", encoding="utf-8") as file:
#             while True:
#                 chunk = file.read(chunk_size)
#                 if not chunk:
#                     break
#                 yield from parse(chunk)

#     def contains_chinese(text):
#         # Regular expression pattern to match Chinese characters
#         chinese_char_pattern = re.compile(r'[\u4e00-\u9fff]+')
#         return bool(chinese_char_pattern.search(text))

#     # List of models to use
#     models = [
#         "nlptown/bert-base-multilingual-uncased-sentiment",
#         "tabularisai/multilingual-sentiment-analysis",
#         # "issai/rembert-sentiment-analysis-polarity-classification-kazakh",
#         "cardiffnlp/twitter-xlm-roberta-base-sentiment",
#         # "uer/roberta-base-finetuned-chinanews-chinese"
#     ]

#     # Create sentiment analysis pipelines for each model
#     classifiers = [pipeline("sentiment-analysis", model=model, device=-1) for model in models]

#     file_path = "inputTest.txt"
#     # file_path = "input.txt"

#     results = []

#     # Populate the processed list by iterating over the generator
#     for sentence in process_file(file_path):
#         print(f"Processed sentence: {sentence}")

#     for i in range(len(processed)):
#         sentence = processed[i]
#         id = ids[i]
#         model_results = {}
#         for classifier, model_name in zip(classifiers, models):
#             result = classifier(sentence)
#             score = result[0]['score']  # Access the score from the first dictionary in the list
#             model_results[model_name] = score
#         mixed = contains_chinese(sentence)
#         results.append({"contents": sentence, "scores": model_results, "mixed": mixed, "id": id})

#     with open("out.json", "w", encoding="utf-8") as out_file:
#         json.dump(results, out_file, ensure_ascii=False, indent=4)

#     # Print the lengths of the ids and processed lists
#     print(f"Length of ids: {len(ids)}")
#     print(f"Length of processed: {len(processed)}")

# except Exception as e:
#     print(f"An error occurred: {e}")