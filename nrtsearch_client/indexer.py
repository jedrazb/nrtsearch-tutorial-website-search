import json
from more_itertools import chunked

from service_discovery import SERVICE_DISCOVERY
from client import get_nrtsearch_client
from client import INDEX_NAME
from setup_index import commit_index
from yelp.nrtsearch.luceneserver_pb2 import AddDocumentRequest

# For prod cases we can make it 1000, takin small value for this tutorial
BATCH_SIZE = 10


# Load the data processed and saved by the crawler
def _load_website_data():
    with open("index_resources/website_data.json") as f:
        data = json.load(f)

    return data


# Prepare the request payload
def _prepare_document_stream(docs):
    for doc in docs:
        fields = {
            "url": AddDocumentRequest.MultiValuedField(value=[doc["url"]]),
            "title": AddDocumentRequest.MultiValuedField(value=[doc["title"]]),
            "description": AddDocumentRequest.MultiValuedField(
                value=[doc["description"]]
            ),
            "headings": AddDocumentRequest.MultiValuedField(value=doc["headings"]),
            "content": AddDocumentRequest.MultiValuedField(value=[doc["content"]]),
        }

        yield AddDocumentRequest(indexName=INDEX_NAME, fields=fields)


# Use gRPC streaming to send documents for ingestion
def index_document_stream(primary_client, doc_stream):
    response = primary_client.addDocuments(doc_stream)
    return response


def run_indexer():
    # Just index data to primary - data will be replicated to other nodes in the cluster
    host, port = SERVICE_DISCOVERY.get("primary-node")
    primary_client = get_nrtsearch_client(host, port)

    website_docs = _load_website_data()

    # Split data into chunks for bulk ingestion
    chunked_website_docs = chunked(website_docs, BATCH_SIZE)

    # Process each chunk of docs in bulk
    for idx, docs_chunk in enumerate(chunked_website_docs):
        doc_stream = _prepare_document_stream(docs=docs_chunk)
        index_response = index_document_stream(primary_client, doc_stream)
        print(
            f"Indexing docs chunk: {idx}, number of docs: {len(docs_chunk)}, response:\n{index_response}"
        )
    # Call commit after docs are ingested
    commit_response = commit_index(primary_client)
    print(f"Commit response:\n{commit_response}")

    print("Successfully indexed data into primary")


if __name__ == "__main__":
    run_indexer()
