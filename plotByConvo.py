import json
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from tqdm import tqdm

# Load the data from out.json
with open('out.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Load models from models.json
with open("models.json", "r", encoding="utf-8") as f:
    models = json.load(f)

# prev = ""
# count = 0
# for entry in data:
#     id = entry["id"]
#     id = id[:5]
#     if(prev != id):
#         prev = IndexError
#         count += 1
# print("convo count: ", count)
# print("data len: ", len(data))

# Process data for each model
for model in models:
    # Group scores by id
    scores_by_id = defaultdict(list)
    for entry in data:
        id = entry["id"][:5]
        score = entry["scores"][model]
        scores_by_id[id].append(score)

    # Sort ids by the mean score within each id group
    sorted_ids = sorted(scores_by_id.keys(), key=lambda x: np.mean(scores_by_id[x]))

    # Prepare data for the boxplot
    sorted_scores = [scores_by_id[id] for id in sorted_ids]
    sorted_means = [np.mean(scores) for scores in sorted_scores]

    # Create the box-and-whisker plot
    plt.figure(figsize=(12, 6))
    plt.boxplot(sorted_scores, vert=True, patch_artist=True, showmeans=True)
    plt.xticks(ticks=range(1, len(sorted_ids) + 1), labels=sorted_ids, rotation=90)
    plt.title(f"Box-and-Whisker Plot of Scores by ID for Model: {model}")
    plt.xlabel("ID (Sorted by Mean Score)")
    plt.ylabel("Score")
    plt.tight_layout()

    # Save or show the plot
    plt.show()