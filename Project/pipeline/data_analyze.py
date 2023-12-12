import json
import pandas as pd
from utils import writeToFile, REVIEWS_PATH, WORDS_PATH, PLOTS_PATH, FINAL_JSON_PATH, TOP_LOCATIONS_PATH
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk

def tokenize_text(text : str) -> list[str]:

    words = [] 
    stop_words = nltk.corpus.stopwords.words('english')
    my_sentences = sent_tokenize(text, "english")

    for sentence in my_sentences:

        # String normalization
        for ponctuation in ['.', ',', '<', '>']:
            sentence = sentence.replace(ponctuation, ' ')
        words_tokenized = word_tokenize(sentence, "english")

        # Filter stop words
        non_stop_words = [word for word in words_tokenized if word.lower() not in stop_words]
        words = words + non_stop_words
    
    return words

def word_segmentation():

    nltk.download('punkt')
    nltk.download('stopwords')

    words_in_reviews = {}
    data = pd.read_json(REVIEWS_PATH)

    for review_index in range(len(data)):

        mytext = data.loc[review_index, 'review_text']

        for word in tokenize_text(mytext):
            if word in words_in_reviews.keys():
                words_in_reviews[word] = words_in_reviews[word] + 1
            else:
                words_in_reviews[word] = 1

    words_in_reviews_dict = {
        "word": words_in_reviews.keys(),
        "count": words_in_reviews.values(),
    }

    writeToFile(WORDS_PATH, pd.DataFrame.from_dict(words_in_reviews_dict))

def word_cloud():

    word_segmentation()
    words = pd.read_json(WORDS_PATH)

    # Sort words frequency
    word_count = []
    for i in range(len(words)):
        word_count.append((words.loc[i, "word"], words.loc[i, "count"]))
    word_count.sort(key=lambda elem: elem[1], reverse=True)

    # Get WordCloud
    LIMIT = 200 
    subset = word_count[:LIMIT]
    wordcloud = WordCloud(width = 800, height = 800,
                          collocations = False,
                          background_color = 'white',
                          min_font_size = 10).generate(' '.join(map(lambda x: (x[0] + " ") * x[1], subset)))

    # WordCloud image
    fig = plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    fig.savefig(PLOTS_PATH + "reviews_wordcloud.png")
    plt.close()

def words_per_review(data_frame, index: int):

    data_frame['word_count'] = data_frame['review_text'].apply(lambda x: len(str(x).split(' ')))
    mean_word_count = data_frame['word_count'].mean()
    limits = {
        1: 800,
        2: 150,
        3: 1000,
        4: 300
    }

    # Bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(data_frame.index, data_frame['word_count'], label='Number of Words')
    plt.axhline(mean_word_count, color='red', linestyle='dashed', label='Mean Word Count')
    plt.text(0, mean_word_count, f'{mean_word_count:.2f}', color='red', va='center', ha='right')
    plt.xlabel('Review Index')
    plt.ylabel('Number of Words')
    plt.title(f'Number of Words in Hotel Reviews {index}')
    plt.ylim(0, limits[index])
    plt.legend()
    plt.savefig(PLOTS_PATH + f'word_count_{index}.png')
    plt.close()

def location_distribution(data):

    data = pd.DataFrame(data)
    location_counts = data['location'].value_counts()

    # 10 most common locations
    top_10_locations = location_counts.head(10)

    top_10_locations.to_csv(TOP_LOCATIONS_PATH)

def rating_distribution(data):

    # Collect hotels average rating
    average_rates = [hotel['average_rate'] for hotel in data]

    # Histogram
    data_frame = pd.DataFrame({'average_rate': average_rates})
    plt.hist(data_frame['average_rate'], bins=range(6), edgecolor='k', alpha=0.7)
    plt.xlabel('Hotel average rate')
    plt.ylabel('Frequency')
    plt.xticks(range(6))

    # Save progress
    plt.savefig(PLOTS_PATH + "rating_distributions.png")
    plt.close()

def date_distribution_years(data):

    # Collect review dates
    review_dates = []
    for hotel in data:
        for review in hotel['reviews']:
            review_dates.append(int(review['date'].split('-')[0]))

    # Histogram
    plt.hist(review_dates, bins=range(2010, 2023), edgecolor='k')
    plt.xlabel('Year')
    plt.ylabel('Frequency')
    plt.title('Reviews distribution by year')
    plt.xlim(2010, 2024)
    plt.savefig(PLOTS_PATH + "date_distributions.png")
    plt.close()

def date_distribution_months(data, selected_year: int):

    # Collect review months
    review_dates = []
    for hotel in data:
        for review in hotel['reviews']:
            [year, month] = review['date'].split('-')
            if int(year) == selected_year:
                review_dates.append(int(month))
    # Histogram
    plt.hist(review_dates, bins=range(1, 14, 1), edgecolor='k')
    plt.xlabel(f'Months {selected_year}')
    plt.ylabel('Frequency')
    plt.title('Reviews distribution by month')
    plt.savefig(PLOTS_PATH + f"date_distributions_{selected_year}.png")
    plt.close()

if __name__ == '__main__':

    data = []
    with open(FINAL_JSON_PATH, 'r') as json_file:
        data = json.load(json_file)
        json_file.close()

    date_distribution_years(data)
    date_distribution_months(data, 2016)
    rating_distribution(data)
    location_distribution(data)
    word_cloud()