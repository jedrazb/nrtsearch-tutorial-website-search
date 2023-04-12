from functools import lru_cache

import grpc

from yelp.nrtsearch.luceneserver_pb2 import CreateIndexRequest
from yelp.nrtsearch.luceneserver_pb2 import IndicesRequest
from yelp.nrtsearch.luceneserver_pb2_grpc import LuceneServerStub


# Simple service discovery
SERVICE_DISCOVERY = {
    "primary-node": ("0.0.0.0", 9000),
    "replica-node-0": ("0.0.0.0", 9001),
    "replica-node-1": ("0.0.0.0", 9002),
}


@lru_cache(3)
def get_nrtsearch_client(host, port):
    channel = grpc.insecure_channel("{0}:{1}".format(host, port))
    return LuceneServerStub(channel)


def run():
    host, port = SERVICE_DISCOVERY.get("primary-node-0")
    client = get_nrtsearch_client(host, port)

    res = client.indices(IndicesRequest())

    print(res)


if __name__ == "__main__":
    run()
