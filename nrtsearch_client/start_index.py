from functools import lru_cache

import grpc

from service_discovery import SERVICE_DISCOVERY
from yelp.nrtsearch.luceneserver_pb2 import CreateIndexRequest
from yelp.nrtsearch.luceneserver_pb2 import IndicesRequest
from yelp.nrtsearch.luceneserver_pb2_grpc import LuceneServerStub


@lru_cache(3)
def get_nrtsearch_client(host, port):
    channel = grpc.insecure_channel("{0}:{1}".format(host, port))
    return LuceneServerStub(channel)


def create_index(nrtsearch_client, index_name):
    nrtsearch_client.createIndex(CreateIndexRequest(indexName=index_name))


def apply_index_settings(nrtsearch_client, settings_dict):
    nrtsearch_client.settings(settings_dict)


def start_index(nrtsearch_client, request_dict):
    pass


def register_fields(nrtsearch_client, schema_dict):
    pass


def configure_and_start_index():
    host, port = SERVICE_DISCOVERY.get("primary-node")
    client = get_nrtsearch_client(host, port)

    res = client.indices(IndicesRequest())

    print(res)


if __name__ == "__main__":
    configure_and_start_index()
