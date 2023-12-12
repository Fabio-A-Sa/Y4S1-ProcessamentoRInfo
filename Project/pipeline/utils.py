import json

HOTELS_PATH = '../data/processed/hotels.json'
REVIEWS_PATH = '../data/processed/reviews.json'
HOTEL_REVIEWS_PATH = '../data/processed/reviews_per_hotel.json'
HOTEL_WORDS_PER_REVIEW_PATH = '../data/analysis/hotel_words_per_review.json'
TOP_LOCATIONS_PATH = '../data/analysis/top_locations.csv'
FINAL_JSON_PATH = '../data/processed/hotels_complete.json'
WORDS_PATH = '../data/analysis/words.json'
PLOTS_PATH = '../data/plots/'

def writeToFile(filename: str, data: json):
    with open(filename, 'w') as file:
        file.write(json.dumps(data.to_dict(orient='records'), indent=2))
        file.close()