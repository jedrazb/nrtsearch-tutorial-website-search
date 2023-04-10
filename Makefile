VENV := venv
PYTHON := $(VENV)/bin/python

$(PYTHON):
	python3 -m venv $(VENV)

venv: $(PYTHON) requirements.txt
	$(PYTHON) -m pip install -r requirements.txt

run_crawler: venv
	$(PYTHON) crawler/crawler.py

clean:
	find . -type d -name "__pycache__" | xargs rm -rf {};
	rm -rf $(VENV)

start_nrtsearch_cluster:
	docker compose --project-directory ./nrtsearch up