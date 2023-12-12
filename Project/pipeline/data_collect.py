import pandas as pd
from utils import writeToFile

def getData(dataset_index: int, attributes: dict):

    data_frame = pd.read_csv(f'../data/raw/hotel_reviews_{dataset_index}.csv', encoding='latin1')

    # Set location column
    if dataset_index == 3:
        data_frame['location'] = 'London'

    # Drop unnecessary columns
    data_frame = data_frame[attributes.keys()].rename(columns=attributes)

    # Save progress
    writeToFile(f'../data/processed/hotel_reviews_{dataset_index}.json', data_frame)

def collect():

    # Select important columns
    getData(1, {'name': 'name', 'city': 'location', 'reviews.date': 'review_date', 'reviews.text': 'review_text', 'reviews.rating': 'review_rate',})
    getData(2, {'Name': 'name', 'Area': 'location', 'Review_Date': 'review_date', 'Review_Text': 'review_text', 'Rating(Out of 10)': 'review_rate'})
    getData(3, {'Property Name': 'name', 'location': 'location', 'Date Of Review': 'review_date', 'Review Text': 'review_text', 'Review Rating': 'review_rate'})
    getData(4, {'Hotel_Name': 'name', 'Hotel_Address': 'location', 'Review_Date': 'review_date', 'Positive_Review': 'positive_review', 'Negative_Review': 'negative_review', 'Reviewer_Score': 'review_rate'})

if __name__ == "__main__":
    collect()