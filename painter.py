import matplotlib.pyplot as plt
import numpy as np

"""BAR CHART VISUALISATION"""
categories = ['Seed 50', 'Seed 100', 'Seed 150']
counts_word2vec = [78, 66, 72]
counts_sense2vec = [79, 84, 76]
x = np.arange(len(categories))

# Width of each bar
bar_width = 0.35

# Plotting the bars for Word2Vec and Sense2Vec
plt.bar(x - bar_width/2, counts_word2vec, width=bar_width, label='Word2Vec', color="green")
plt.bar(x + bar_width/2, counts_sense2vec, width=bar_width, label='Sense2Vec', color="red")

# Adding labels on the bars for Word2Vec
for i, count in enumerate(counts_word2vec):
    plt.text(i - bar_width/2, count, str(count), ha='center', va='bottom')

# Adding labels on the bars for Sense2Vec
for i, count in enumerate(counts_sense2vec):
    plt.text(i + bar_width/2, count, str(count), ha='center', va='bottom')

plt.xlabel('Results')
plt.ylabel('Count')
plt.title('Games completed in each seed - Word2Vec vs Sense2Vec')

plt.xticks(x, categories)
plt.legend(fontsize='small')
plt.grid(axis='y')
plt.show()


"""MATRIX VISUALISATION"""
# Full experiment data collected
data = [
    ['', 'Seed 50 W2V', 'Seed 50 S2V', 'Seed 100 W2V', 'Seed 100 S2V', 'Seed 150 W2V', 'Seed 150 S2V'],
    ['Average Turn', 4.125, 6.28, 3.94, 5.89, 4.33, 5.86],
    ['Minimum # of Turn', 3, 5, 3, 5, 3, 4],
    ['Total Clues', 211, 208, 194, 264, 204, 205],
    ['Correct Guesses', 174, 190, 164, 218, 174, 178],
    ['Total Clues (SR)', 85, 85, 82, 81, 83, 86],
    ['Correct Guesses (SR)', 76, 69, 75, 71, 74, 79],
    ['Assassin Game', 12, 11, 24, 6, 18, 14]
]

labels = [row[0] for row in data[1:]]
models = data[0][1:]
values = [row[1:] for row in data[1:]]

# Plotting the matrix
plt.figure(figsize=(10, 6))
plt.imshow(values, cmap='viridis', aspect='auto')

# Displaying values in each cell
for i in range(len(labels)):
    for j in range(len(models)):
        plt.text(j, i, str(values[i][j]), ha='center', va='center', color='white')

# Add colour bar to the side
cbar = plt.colorbar()
cbar.set_label('Values')

plt.xticks(range(len(models)), models, rotation=45, ha='right')
plt.yticks(range(len(labels)), labels)
plt.title('Experiment data collected across all seeds')
plt.tight_layout()
plt.show()



