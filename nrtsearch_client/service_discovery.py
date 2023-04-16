# Simple service discovery - used for indexer running on the host machine
# This is NOT used for communication between containers
# Within docker containers you access primary node at: primary-node:8000
# replicas at: replica-node:8000
SERVICE_DISCOVERY = {
    "primary-node": ("localhost", 8000),
    "replica-node-0": ("localhost", 8001),
    "replica-node-1": ("localhost", 8002),
}
