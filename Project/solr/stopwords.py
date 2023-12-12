import nltk
import os

FILE_PATH = "../solr/stopwords.txt"

def stopwords():

    stop_words = nltk.corpus.stopwords.words('english')

    with open(FILE_PATH, 'w') as f:
        for word in stop_words:
            f.write(word + "\n")
        f.close()

if __name__ == '__main__':
    if not os.path.exists(FILE_PATH):
        stopwords()