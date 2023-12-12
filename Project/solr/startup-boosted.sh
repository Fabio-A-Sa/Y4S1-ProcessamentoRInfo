#!/bin/bash

# To avoid problems with duplicated containers
docker stop privago
docker rm privago

# Copy pipeline output to virtual "data" folder
cp ../data/processed/hotels_complete.json .

# Running Solr container
# Creating "privago"
# Creating a virtual folder "data"
# Creating "hotels" core/collection
docker run -p 8983:8983 --name privago -v "$(pwd)":/data -d solr:9.3 solr-precreate hotels
sleep 10

docker cp synonyms_reviews.txt privago:/var/solr/data/hotels/conf
sleep 3

# Creating a schema based on "schema-boosted.json" file into "privago"
curl -X POST -H 'Content-type:application/json' --data-binary "@./schema-boosted.json" http://localhost:8983/solr/hotels/schema
sleep 1

# Populate collection using mapped folder "data" and pipeline output
docker exec -it privago bin/post -c hotels -format solr /data/hotels_complete.json
sleep 1

# Removing always pipeline output for github/commits reasons
rm hotels_complete.json
