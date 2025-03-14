from transformers import pipeline, AutoTokenizer

import re
import torch

file = open("inputTest.txt", "r", encoding="utf-8")
input = file.read()

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
tokens = tokenizer.tokenize(input)
print(tokens)