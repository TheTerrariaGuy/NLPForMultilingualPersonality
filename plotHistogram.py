import json
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter, defaultdict

# Parse the out.json file
with open('out.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Load models from models.json
with open("models.json", "r", encoding="utf-8") as f:
    models = json.load(f)

# Go over each model and create percentage-based grouped bar plots
for model in models:
    # Group labels by their 'mixed' category
    grouped_label_counts = defaultdict(Counter)
    for entry in data:
        mixed_category = entry['mixed']  # 0: EN Only, 1: CN Only, 2: Mixed
        label = entry['scores'][model]
        grouped_label_counts[mixed_category][label] += 1

    # Prepare data for the grouped bar plot
    categories = ['EN Only', 'CN Only', 'Mixed']
    labels = set()  # Collect all unique labels across categories
    for counts in grouped_label_counts.values():
        labels.update(counts.keys())
    labels = sorted(labels)  # Sort labels for consistent ordering

    # Calculate total counts for each category
    total_counts = {category: sum(grouped_label_counts[i].values()) for i, category in enumerate(categories)}

    # Create percentage arrays for each category
    percentages = {
        category: [
            (grouped_label_counts[i][label] / total_counts[category] * 100 if total_counts[category] > 0 else 0)
            for label in labels
        ]
        for i, category in enumerate(categories)
    }

    # Plot grouped bar chart
    x = np.arange(len(labels))  # X positions for the labels
    bar_width = 0.25  # Width of each bar

    plt.figure(figsize=(12, 6))
    for i, category in enumerate(categories):
        plt.bar(x + i * bar_width, percentages[category], width=bar_width, label=category)

    # Add labels and legend
    plt.xticks(x + bar_width, labels, rotation=45, ha='right')  # Center the ticks between bars
    plt.title(f'Percentage Distribution of Labels for {model}')
    plt.xlabel('Labels')
    plt.ylabel('Percentage (%)')
    plt.legend(title='Category')
    plt.tight_layout()

    # Show or save the plot
    plt.show()