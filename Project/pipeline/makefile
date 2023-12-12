all: clean requirements collect normalize merge sample analyze

clean:
	rm -rf ../data/processed
	rm -rf ../data/analysis
	rm -rf ../data/plots

requirements:
	pip3 install -r requirements.txt

collect:
	mkdir -p ../data/processed
	python3 data_collect.py

normalize:
	mkdir -p ../data/plots
	python3 data_normalize.py

merge:
	python3 data_merge.py

sample:
	python3 data_sample.py

analyze:
	mkdir -p ../data/analysis
	python3 data_analyze.py

semantic:
	cat ../data/processed/hotels_complete.json | python3 get_embeddings.py > ../data/processed/semantic_hotels.json
