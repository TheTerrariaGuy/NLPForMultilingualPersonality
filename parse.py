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