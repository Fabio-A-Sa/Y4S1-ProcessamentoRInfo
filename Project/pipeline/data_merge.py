import json
import pandas as pd
from utils import writeToFile, REVIEWS_PATH

def merge(indexes):   
    
    all_data = []
    for index in indexes:
        with open(f'../data/processed/hotel_reviews_{index}.json', 'r') as file:
            all_data.extend(json.load(file))
            file.close()

    writeToFile(REVIEWS_PATH, pd.DataFrame(all_data))

if __name__ == '__main__':
    merge([x for x in range(1, 5)])