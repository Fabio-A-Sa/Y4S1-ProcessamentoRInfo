import pandas as pd
import numpy as np
import math
import random
import matplotlib.pyplot as plt
from unidecode import unidecode
from utils import PLOTS_PATH, writeToFile, HOTELS_PATH, REVIEWS_PATH, HOTEL_REVIEWS_PATH, FINAL_JSON_PATH


def remove_duplicates():
    hotel_reviews = pd.read_json(REVIEWS_PATH)
    hotel_reviews.drop_duplicates(subset=['review_text'], inplace=True)
    hotel_reviews.reset_index(drop=True, inplace=True)
    writeToFile(REVIEWS_PATH, hotel_reviews)


def hotels_average_rate():

    hotel_reviews = pd.read_json(REVIEWS_PATH)
    grouped_reviews_rate = hotel_reviews.groupby('name').agg({'review_rate': 'mean', 'location': 'first'}).reset_index().round(2)
    grouped_reviews_rate.rename(
        columns={'review_rate': 'average_rate'}, inplace=True
    )

    writeToFile(HOTELS_PATH, grouped_reviews_rate)

def reviews_per_hotel():
    hotel_reviews = pd.read_json(REVIEWS_PATH)
    hotels = pd.read_json(HOTELS_PATH)

    hotels_dict = {}
    for h in range(len(hotels)):
        hotels_dict[ hotels.loc[h, "name"] ] = 0 # number_of_reviews
    
    for r in range(len(hotel_reviews)):
        if hotel_reviews.loc[r, "name"] not in hotels_dict.keys():
            print(f'{hotel_reviews.loc[r, "name"]} not in the hotels list!') 
            continue

        hotels_dict[ hotel_reviews.loc[r, "name"] ] = hotels_dict[ hotel_reviews.loc[r, "name"] ] + 1

    reviews_per_hotel_dict = {
        "hotel": hotels_dict.keys(),
        "reviews": hotels_dict.values(),
    }

    description = pd.DataFrame.from_dict(reviews_per_hotel_dict)["reviews"].describe()
    writeToFile(HOTEL_REVIEWS_PATH, pd.DataFrame.from_dict(reviews_per_hotel_dict))
    return(int(description['25%']), int(description['75%']))


def draw_hotel_reviews_number(hotel_reviews : pd.DataFrame):
    # Bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(hotel_reviews.index, hotel_reviews['reviews'], label='Number of Reviews')
    plt.xlabel('Hotel Index')
    plt.ylabel('Number of Reviews')
    plt.title(f'Number of Reviews per Hotel')
    plt.ylim(0, 1500)
    plt.legend()
    plt.savefig(PLOTS_PATH + f'hotel_reviews_number.png')
    plt.close()

def limit_hotel_reviews(inferior_limit: int, superior_limit: int):
    hotel_reviews = pd.read_json(HOTEL_REVIEWS_PATH)
    hotel_reviews = hotel_reviews[(hotel_reviews['reviews'] >= inferior_limit)]

    draw_hotel_reviews_number(hotel_reviews)

    purge_reviews(superior_limit)
    
    #update purged review numbers
    reviews = pd.read_json(REVIEWS_PATH)

    for index, hotel_reviews_obj in hotel_reviews.iterrows():

        hotel_name = hotel_reviews_obj["hotel"]

        reviews_number = len(reviews[(reviews["name"] == hotel_name)])

        hotel_reviews.loc[index, "reviews"] = reviews_number

    writeToFile(HOTEL_REVIEWS_PATH, pd.DataFrame.from_dict(hotel_reviews))

def final_json():

    reviews_per_hotel = pd.read_json(HOTEL_REVIEWS_PATH)
    hotels = pd.read_json(HOTELS_PATH)
    reviews = pd.read_json(REVIEWS_PATH)
    
    hotels_info = []
    for _, review_per_hotel in reviews_per_hotel.iterrows():
        hotel_name = review_per_hotel['hotel']
        hotel_info = hotels[hotels['name'] == hotel_name].to_dict(orient='records')[0]
        hotels_info.append({
            'name': hotel_info['name'],
            'location': hotel_info['location'],
            'average_rate': hotel_info['average_rate'],
            'reviews': []
        })

    for _, review in reviews.iterrows():
        hotel_name = review['name']
        for a in hotels_info:
            if hotel_name == a['name']:
                a['reviews'].append({
                    'date': review['review_date'],
                    'rate': review['review_rate'],
                    'text': review['review_text'],
                })

    writeToFile(FINAL_JSON_PATH, pd.DataFrame.from_dict(hotels_info))
    
# eliminar reviews
def purge_reviews(max_reviews_number: int):
    hotels_reviews = pd.read_json(HOTEL_REVIEWS_PATH)
    reviews = pd.read_json(REVIEWS_PATH)

    hotels_to_purge = []

    for i in range(len(hotels_reviews)):
        if (hotels_reviews.loc[i, "reviews"] > max_reviews_number):
            hotels_to_purge.append(hotels_reviews.loc[i, "hotel"])


    for hotel_to_purge in hotels_to_purge:
        reviews_to_purge = reviews.loc[reviews["name"] == hotel_to_purge]

        review_rates = {}
        for r in reviews_to_purge.index.tolist():
            if (reviews_to_purge.loc[r, "review_rate"] in review_rates.keys()):
                review_rates[ reviews_to_purge.loc[r, "review_rate"] ] = review_rates[ reviews_to_purge.loc[r, "review_rate"] ] + 1
            else:
                review_rates[ reviews_to_purge.loc[r, "review_rate"] ] = 1
            
        
        # deciding how many reviews in each rate are going to be deleetd

        result = [math.floor((rev/len(reviews_to_purge)) * max_reviews_number) for rev in review_rates.values()]
        result_rest = [(rev/len(reviews_to_purge)) * max_reviews_number - math.floor((rev/len(reviews_to_purge)) * max_reviews_number) for rev in review_rates.values()]
        
        idx_added = []
        
        for i in range(max_reviews_number - sum(result)):
            highest = -1
            for j in range(len(result)):
                if highest < 0:
                    if j in idx_added:
                        continue
                    else:
                        highest = j
                if (result_rest[highest] < result_rest[j] and j not in idx_added):
                    highest = j
            
            idx_added.append(highest)
        
        for idx in idx_added:
            result[idx] = result[idx] + 1

        # deleting reviews
        new_review_rates = {}

        for i in range(len(review_rates.keys())):
            new_review_rates[list(review_rates.keys())[i]] = result[i]
        
        for key in review_rates:
            diff = review_rates[key] - new_review_rates[key]
            if not diff: continue

            # choose which rows to drop
            idxs_to_purge = reviews_to_purge[reviews_to_purge["review_rate"] == key]
            idxs_to_purge = random.sample(idxs_to_purge.index.tolist(), diff)

            # drop the choosen rows
            reviews = reviews.drop(index=idxs_to_purge)
        
    
    writeToFile(REVIEWS_PATH, reviews)




if __name__ == '__main__':
    remove_duplicates()
    hotels_average_rate()
    limits = reviews_per_hotel()
    limit_hotel_reviews(limits[0], limits[1])
    final_json()