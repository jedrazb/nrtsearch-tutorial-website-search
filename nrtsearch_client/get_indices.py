from service_discovery import SERVICE_DISCOVERY
from client import get_nrtsearch_client
from client import INDEX_NAME
from yelp.nrtsearch.luceneserver_pb2 import IndicesRequest


def get_indices(client):
    response = client.indices(IndicesRequest())
    return response


def run():
    for service, (host, port) in SERVICE_DISCOVERY.items():
        client = get_nrtsearch_client(host, port)
        print(f"IndicesRequest for: {service}")
        indices_response = get_indices(client)
        print(indices_response)


if __name__ == "__main__":
    run()
