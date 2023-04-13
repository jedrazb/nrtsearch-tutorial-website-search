VENV := venv
PYTHON := $(VENV)/bin/python

$(PYTHON):
	python3 -m venv $(VENV)

venv: $(PYTHON) requirements.txt
	$(PYTHON) -m pip install -r requirements.txt

clean:
	find . -type d -name "__pycache__" | xargs rm -rf {};
	rm -rf $(VENV)

# Crawler
run_crawler:
	$(PYTHON) crawler/crawler.py

# Nrtsearch cluster
start_nrtsearch_cluster:venv
	docker compose --project-directory ./nrtsearch up

# Generate nrtsearch .proto files and their dependencies
nrtsearch_protos:
	mkdir -p protos 
	docker build -t nrtsearch-protos-builder:latest ./utils/nrtsearch_protos_builder/
	docker run -v $(shell pwd)/protos:/user/protos  nrtsearch-protos-builder:latest

# Compile client .proto files to python code
nrtsearch_protoc: nrtsearch_protos
	$(PYTHON) -m grpc_tools.protoc \
		--proto_path protos \
		--grpc_python_out nrtsearch_client \
		--python_out nrtsearch_client \
		protos/yelp/nrtsearch/luceneserver.proto \
		protos/yelp/nrtsearch/search.proto \
		protos/yelp/nrtsearch/analysis.proto \
		protos/yelp/nrtsearch/suggest.proto
	rm -rf protos


# Setup index on primary and replicas
setup_index:
	$(PYTHON) nrtsearch_client/setup_index.py

# Index the data into nrtsearch
run_indexer: run_crawler
	$(PYTHON) nrtsearch_client/indexer.py


