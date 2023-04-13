from functools import lru_cache

import grpc

from yelp.nrtsearch.luceneserver_pb2_grpc import LuceneServerStub


INDEX_NAME = "blog_search"


@lru_cache(3)
def get_nrtsearch_client(host, port):
    channel = grpc.insecure_channel(f"{host}:{port}")
    return LuceneServerStub(channel)
