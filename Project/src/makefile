all: requirements solr web

requirements:
	npm install

solr:
	cd ../solr && \
	chmod +x startup-final.sh && \
	bash startup-final.sh && \
	sleep 5
	cd ../src

web:
	node privago.js 3000