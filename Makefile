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
run_crawler: venv
	$(PYTHON) crawler/crawler.py

# Nrtsearch cluster
start_nrtsearch_cluster:
	docker compose --project-directory ./nrtsearch up

# Generate nrtsearch .proto files and their dependencies
nrtsearch_protos:
	mkdir -p protos 
	docker build -t nrtsearch-protos-builder:latest ./utils/nrtsearch_protos_builder/
	docker run -v $(shell pwd)/protos:/user/protos  nrtsearch-protos-builder:latest

# Compile client .proto files to python code
nrtsearch_protoc: nrtsearch_protos
	mkdir -p protoc
	$(PYTHON) -m grpc_tools.protoc \
		--proto_path protos \
		--grpc_python_out protoc \
		--python_out protoc \
		protos/yelp/nrtsearch/luceneserver.proto \
		protos/yelp/nrtsearch/search.proto \
		protos/yelp/nrtsearch/analysis.proto \
		protos/yelp/nrtsearch/suggest.proto
	cp `find protoc -name "*.py"` nrtsearch_client/nrtsearch_py_grpc
	rm -rf protos protoc




