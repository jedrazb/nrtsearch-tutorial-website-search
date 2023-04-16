VENV := venv
PYTHON := $(VENV)/bin/python

$(PYTHON):
	python3 -m venv $(VENV)

venv: $(PYTHON) requirements.txt
	$(PYTHON) -m pip install -r requirements.txt

clean:
	find . -type d -name "__pycache__" | xargs rm -rf {};
	rm -rf $(VENV)
	docker compose rm -sfv

# Nrtsearch Tutorial - Blog Search
start: nrtsearch_protoc
	mkdir -p logs
	cp requirements.txt ./nrtsearch_client/requirements.txt
	docker compose build
	docker compose up

# Crawler
run_crawler: venv
	$(PYTHON) crawler/crawler.py

# Generate nrtsearch .proto files and their dependencies
nrtsearch_protos:
	mkdir -p protos 
	docker build -t nrtsearch-protos-builder:latest ./utils/nrtsearch_protos_builder/
	docker run -v $(shell pwd)/protos:/user/protos  nrtsearch-protos-builder:latest

# Compile client .proto files to python code
nrtsearch_protoc: venv nrtsearch_protos
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
start_index: venv
	$(PYTHON) nrtsearch_client/setup_index.py

# Index the data into nrtsearch
run_indexer: venv
	$(PYTHON) nrtsearch_client/indexer.py

# Check index status
index_status: venv
	$(PYTHON) nrtsearch_client/get_indices.py


