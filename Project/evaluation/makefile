all: requirements query evaluation

requirements:
	pip3 install -r requirements.txt

query:	
	python3 ../solr/synonyms.py
	python3 ../solr/stopwords.py
	python3 query.py m3

evaluation:
	python3 -m spacy download en_core_web_sm
	python3 morelikethis.py
	python3 evaluation.py m3 > stats.json