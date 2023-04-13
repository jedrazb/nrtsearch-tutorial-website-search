import json
from yaml import load, Loader
from google.protobuf.json_format import Parse

from service_discovery import SERVICE_DISCOVERY
from client import get_nrtsearch_client
from yelp.nrtsearch.luceneserver_pb2 import CreateIndexRequest
from yelp.nrtsearch.luceneserver_pb2 import CommitRequest
from yelp.nrtsearch.luceneserver_pb2 import StartIndexRequest
from yelp.nrtsearch.luceneserver_pb2 import SettingsRequest
from yelp.nrtsearch.luceneserver_pb2 import FieldDefRequest

INDEX_NAME = "blog_search"
INDEX_SCHEMA_PATH = "index_resources/index_schema.yaml"
INDEX_SETTINGS_PATH = "index_resources/index_settings.yaml"


def create_index(nrtsearch_client):
    response = nrtsearch_client.createIndex(CreateIndexRequest(indexName=INDEX_NAME))
    return response


def apply_index_settings(nrtsearch_client, settings_dict):
    settings_request = Parse(json.dumps(settings_dict), SettingsRequest())
    response = nrtsearch_client.settings(settings_request)
    return response


def start_index_primary(nrtsearch_primary_client):
    response = nrtsearch_primary_client.startIndex(
        StartIndexRequest(indexName=INDEX_NAME, mode=1)  # PRIMARY
    )
    return response


def start_index_replica(
    nrtsearch_replica_client,
):
    response = nrtsearch_replica_client.startIndex(
        StartIndexRequest(
            indexName=INDEX_NAME,
            mode=2,  # REPLICA
            primaryAddress="primary-node",  # docker address, can be resolved from container
            port=8001,  # replication port
        )
    )
    return response


def register_fields(nrtsearch_client, index_schema_dict):
    register_fields_req = Parse(json.dumps(index_schema_dict), FieldDefRequest())
    response = nrtsearch_client.registerFields(register_fields_req)
    return response


def commit_index(nrtsearch_client):
    response = nrtsearch_client.commit(CommitRequest(indexName=INDEX_NAME))
    return response


def _load_index_schema():
    with open(INDEX_SCHEMA_PATH, "r") as f:
        stream = f.read()
    schema = load(stream, Loader=Loader)
    return schema


def _load_index_settings():
    with open(INDEX_SETTINGS_PATH, "r") as f:
        stream = f.read()
    settings = load(stream, Loader=Loader)
    return settings


def setup_primary_index():
    host, port = SERVICE_DISCOVERY.get("primary-node")
    primary_client = get_nrtsearch_client(host, port)

    print("Starting index on the primary node")

    create_index_res = create_index(primary_client)
    print(create_index_res)

    apply_settings_res = apply_index_settings(primary_client, _load_index_settings())
    print(apply_settings_res)

    start_index_res = start_index_primary(primary_client)
    print(start_index_res)

    register_fields_res = register_fields(primary_client, _load_index_schema())
    print(register_fields_res)

    commit_res = commit_index(primary_client)
    print(commit_res)

    print("DONE: index started in the primary node")


def setup_replicas_index():
    replica_clients = []
    for replica_service in ["replica-node-0", "replica-node-1"]:
        host, port = SERVICE_DISCOVERY.get(replica_service)
        client = get_nrtsearch_client(host, port)
        replica_clients.append(client)

    print("Starting index on the replica nodes")

    for replica_client in replica_clients:
        create_index_res = create_index(replica_client)
        print(create_index_res)

        apply_settings_res = apply_index_settings(
            replica_client, _load_index_settings()
        )
        print(apply_settings_res)

        start_index_res = start_index_replica(
            replica_client,
        )
        print(start_index_res)

        register_fields_res = register_fields(replica_client, _load_index_schema())
        print(register_fields_res)

        commit_res = commit_index(replica_client)
        print(commit_res)

    print("DONE: index started in the replica nodes")


def run():
    """
    Note: this method depends on the cluster state. It will work on a fresh cluster without blog_search index present.
    If you wish to run this method again, you must run clean up docker volumes:
    - docker compose --project-directory nrtsearch rm
    """

    # Setup index on primary
    setup_primary_index()

    # Setup index on replicas
    setup_replicas_index()


if __name__ == "__main__":
    run()
