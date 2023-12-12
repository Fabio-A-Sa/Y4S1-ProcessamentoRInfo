import matplotlib.pyplot as plt
import numpy as np
import spacy
import json

NPL = spacy.load("en_core_web_sm")
SOLR_RESULTS_PATH = "./mlt/results.json"
SOLR_EVALUATION_PATH = './mlt/evaluation.json'
PLOTS_PATH = './mlt'

def calculate_similarity(review, similar_texts):
    doc1 = NPL(review)
    similarities = []

    for text in similar_texts:
        doc2 = NPL(text)
        similarity = round(doc1.similarity(doc2), 3)
        similarities.append(similarity)

    return similarities

def plot_evaluation(results):

    query_means = [np.mean(results[i]) for i in range(1, 21)]              # Mean by query
    global_mean = np.mean([np.mean(results[i]) for i in range(1, 21)])     # Global mean

    # Bar chart of the overall similarity percentage for each query
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(1, 21)
    bar_width = 0.4
    ax.bar(x, [mean * 100 for mean in query_means], bar_width, label='Query average')

    # Global line
    ax.axhline(global_mean * 100, color='red', linestyle='dashed', linewidth=2, label=f'Global average = {global_mean * 100:.2f}')

    # Labels
    ax.set_xlabel('Query')
    ax.set_ylabel('Mean percentage (%)')
    ax.set_title('Overall similarity percentage for each query')
    ax.set_xticks(x)
    ax.legend()
    plt.savefig(f'{PLOTS_PATH}/mean_similiarity.png')
    plt.close()

    # Evolution chart of similarity for each query across result indexes
    fig, ax = plt.subplots(figsize=(10, 6))
    for i in range(1, 21):
        ax.plot(np.arange(1, 11), [result * 100 for result in results[i]], marker='o', label=f'Query {i}')

    # Labels
    ax.set_xlabel('Result index')
    ax.set_ylabel('Percentage (%)')
    ax.set_title('Evolution of similarity for each query across result indexes')
    ax.legend()
    ax.set_ylim(0, 100)
    plt.savefig(f'{PLOTS_PATH}/similiarity_evolution.png')
    plt.close()

    # Evolution chart of average similarity across result indexes
    average_results = [np.mean([results[j][i] for j in range(1, 21)]) * 100 for i in range(10)]
    plt.figure(figsize=(10, 6))
    plt.plot(np.arange(1, 11), average_results, marker='o', linestyle='-', color='green', label='Average similiarity across indexes')

    # Labels
    plt.xlabel('Result index')
    plt.ylabel('Percentage (%)')
    plt.title('Evolution of average similarity across result indexes')
    plt.legend()
    plt.ylim(0, 100)
    plt.savefig(f'{PLOTS_PATH}/similiarity_average_evolution.png')
    plt.close()

def save_evaluation(evaluation):
    
    results = dict()
    for (i, (_, similiarities)) in enumerate(evaluation):
        print(f"{i+1}: {similiarities}")
        results[i+1] = similiarities

    with open(SOLR_EVALUATION_PATH, 'w') as file:
        json.dump(results, file, indent=2)
        file.close()

    plot_evaluation(results)

def main():

    # Get solr results
    results = []
    with open(SOLR_RESULTS_PATH, 'r') as file:
        results = json.load(file)
        file.close()

    # Evaluation based on similiarity
    evaluation = []
    for entry in results:
        review = entry['review']
        similar_texts = entry['related']
        similarities = calculate_similarity(review, similar_texts)
        evaluation.append([review, similarities])

    # Save progress
    save_evaluation(evaluation)

if __name__ == "__main__":
    main()
