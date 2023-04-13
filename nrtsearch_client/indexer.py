import json
from more_itertools import chunked

from service_discovery import SERVICE_DISCOVERY
from client import get_nrtsearch_client
from client import INDEX_NAME
from setup_index import commit_index
from yelp.nrtsearch.luceneserver_pb2 import AddDocumentRequest

# For prod cases we can make it 1000, takin small value for this tutorial
BATCH_SIZE = 10


def _load_website_data():
    with open("index_resources/website_data.json") as f:
        data = json.load(f)

    return chunked(data, BATCH_SIZE)


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


def index_document_stream(primary_client, doc_stream):
    # We are streaming docs in bulk for ingestion
    response = primary_client.addDocuments(doc_stream)
    return response


def run_indexer():
    # Just index data to primary - data will be replicated to other nodes in the cluster
    host, port = SERVICE_DISCOVERY.get("primary-node")
    primary_client = get_nrtsearch_client(host, port)

    website_docs_chunks = _load_website_data()

    for idx, docs_chunk in enumerate(website_docs_chunks):
        doc_stream = _prepare_document_stream(docs=docs_chunk)
        index_response = index_document_stream(primary_client, doc_stream)
        print(
            f"Indexing docs chunk: {idx}, number of docs: {len(docs_chunk)}, response:\n{index_response}"
        )

    commit_response = commit_index(primary_client)
    print(f"Commit response:\n{commit_response}")

    print("Successfully indexed data into primary")


if __name__ == "__main__":
    run_indexer()
