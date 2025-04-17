import json
import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np  # Import NumPy for calculating averages

# Parse the out.json file
with open('out.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Load models from models.json
with open("models.json", "r", encoding="utf-8") as f:
    models = json.load(f)

# Go over each model and do t-tests
for model in models:
    # Wrangle the data
    en_only_scores = [entry['scores'][model] for entry in data if entry['mixed'] == 0]
    cn_only_scores = [entry['scores'][model] for entry in data if entry['mixed'] == 1]
    mixed_scores = [entry['scores'][model] for entry in data if entry['mixed'] == 2]

    # Calculate averages
    avg_en_only = np.mean(en_only_scores) if en_only_scores else 0
    avg_cn_only = np.mean(cn_only_scores) if cn_only_scores else 0
    avg_mixed = np.mean(mixed_scores) if mixed_scores else 0

    # Do t-tests
    t_stat_en_cn, p_value_en_cn = stats.ttest_ind(en_only_scores, cn_only_scores, equal_var=False)
    t_stat_en_mixed, p_value_en_mixed = stats.ttest_ind(en_only_scores, mixed_scores, equal_var=False)
    t_stat_cn_mixed, p_value_cn_mixed = stats.ttest_ind(cn_only_scores, mixed_scores, equal_var=False)

    # Print results
    print(f"Model: {model}")
    print(f"Average (EN Only): {avg_en_only:.4f}")
    print(f"Average (CN Only): {avg_cn_only:.4f}")
    print(f"Average (Mixed): {avg_mixed:.4f}")
    print(f"T-statistic (EN vs CN): {t_stat_en_cn:.4f}, P-value: {p_value_en_cn}")
    print(f"T-statistic (EN vs Mixed): {t_stat_en_mixed:.4f}, P-value: {p_value_en_mixed}")
    print(f"T-statistic (CN vs Mixed): {t_stat_cn_mixed:.4f}, P-value: {p_value_cn_mixed}")
    print("-" * 50)

    # Plot data
    plt.figure(figsize=(10, 6))
    plt.hist(en_only_scores, alpha=0.5, label=f'EN Only (Avg: {avg_en_only:.2f})', bins=20)
    plt.hist(cn_only_scores, alpha=0.5, label=f'CN Only (Avg: {avg_cn_only:.2f})', bins=20)
    plt.hist(mixed_scores, alpha=0.5, label=f'Mixed (Avg: {avg_mixed:.2f})', bins=20)
    plt.legend(loc='upper right')
    plt.title(f'Histogram of Scores for {model}')
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.show()



