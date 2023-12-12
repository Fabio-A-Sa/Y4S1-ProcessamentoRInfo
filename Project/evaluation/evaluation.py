import json
import matplotlib.pyplot as plt
from sklearn.metrics import PrecisionRecallDisplay
import sys

LIMIT = 20
PRECISION_AT = 20
QUERIES = 8

MODES = {
    'm2': ['simple', 'boosted'],
    'm3': ['boosted', 'stopwords', 'semantic', 'final']
}

def getResults(query: int, mode: str) -> list:
    path = f"./q{query}/evaluation-{mode}.json"
    with open(path, 'r') as file:
        data = json.load(file)
        file.close()
    
    results = data.values()
    assert len(results) == LIMIT
    return list(results)

def recall_at_k(results: list, k: int) -> float:
    return len([
        result for result in results[:k] if result == 1
    ]) / len(results)

def precision_values(results: list) -> float:
    return [
        len([
            doc for doc in results[:idx] if doc == 1
        ]) / idx 
        for idx, _ in enumerate(results, start=1)
    ]

def recall_values(results: list) -> float:
    return [
        (len([
            doc for doc in results[:idx] if doc == 1
        ]) / sum(results)) if sum(results) else 0
        for idx, _ in enumerate(results, start=1)
    ]

# MAP
def mean_average_precision(stats, modes):

    result = {mode: 0 for mode in modes}
    count = {mode: 0 for mode in modes}
    
    for entry in stats:
        mode = entry["mode"]
        average_precision = entry["AvP"]
        
        if mode in modes:
            result[mode] += average_precision
            count[mode] += 1

    for mode in modes:
        result[mode] /= count[mode] if count[mode] > 0 else 1
    
    return result

# P@K - Precision At K
def precision_at_k(results: list, k: int = PRECISION_AT) -> float:
    return len([
        result for result in results[:k] if result == 1
    ]) / k

# AvP - Average Precision
def average_precision(results: list) -> float:
    precisions = precision_values(results)
    return round(sum(precisions) / len(results), 2)

# Recall
def recall(results: list) -> float:
    return round(sum(recall_values(results)), 2)

# Accumulative curves
def acc_results(precision, recall):
    maximos = []

    for _, r in zip(precision, recall):
        max_precision = max([p_i for (p_i, r_i) in zip(precision, recall) if r_i >= r])
        maximos.append(max_precision)

    return maximos

# Precision-Recall Curves
def precision_recall(results: list, mode: str, query: int) -> None:

    precision_results = [round(v, 2) for v in precision_values(results)]
    recall_results = [round(v, 2) for v in recall_values(results)]

    x = [round(0.05 * x, 2) for x in range(1, 21)]
    y = acc_results(precision_results, recall_results)

    plt.xlim(0, 1.1)
    plt.ylim(0, 1.1)

    plt.plot(x, y, label='Precision-Recall Curve')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title(f'Precision-Recall Curve Q{query} ({mode} mode)')
    plt.legend()
    plt.savefig(f'./q{query}/p-r-curve-{mode}.png')
    plt.close()

def compute_rcs(results: dict, query: int):
    for k, v in results.items():
        precision_recall(v, k, query)

def print_stats(stats: dict) -> None:
    for key, value in stats.items():
        print(f"{key}: {value}")

def evaluate(query: int, mode: str) -> None:

    results = getResults(query, mode)
    stats = {
        'query': f'q{query}',
        'mode': mode,
        f'P@{PRECISION_AT}': precision_at_k(results),
        'AvP': average_precision(results),
    }

    return [stats, results]

if __name__ == "__main__":

    # Milestones Global Evaluation
    if len(sys.argv) == 2 and sys.argv[1].lower() in ['m2', 'm3']:

        stats = []
        results = {}
        milestone = sys.argv[1].lower()
        [min, max] = [1, 4] if milestone == 'm2' else [5, 8]
        for query in range(min, max + 1):
            for mode in MODES[milestone]:
                output = evaluate(query, mode)
                stats.append(output[0])
                results[mode] = output[1]
            compute_rcs(results, query)

        output = {
            'Results per query and per mode': stats,
            'Global MAP': mean_average_precision(stats, MODES[milestone]),
        }
        
        print(json.dumps(output, indent=2))

    # Run a single evaluation
    elif len(sys.argv) == 2 and 1 <= int(sys.argv[1]) <= 8:

        stats = []
        results = {}
        modes = MODES['m2'] if int(sys.argv[1]) < 5 else MODES['m3']
        for mode in modes:
            output = evaluate(int(sys.argv[1]), mode)
            stats.append(output[0])
            results[mode] = output[1]
        compute_rcs(results, int(sys.argv[1]))

        print("Stats per query and per mode")
        print(json.dumps(stats, indent=2))

    # Error
    else:
        print("Bad arguments. Usage:")
        print("   python3 evaluation.py M<2,3>       - for global milestone evaluation")
        print("   python3 evaluation.py <1,2,3,4>    - for individual evaluation of milestone 2 queries")
        print("   python3 evaluation.py <5,6,7,8>    - for individual evaluation of milestone 3 queries")
