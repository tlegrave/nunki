import json
import os

import redis

from .. import repository

redis_url = os.getenv("REDIS_URL", "localhost")
redis_port = os.getenv("REDIS_PORT", 6379)


def list_posts_on_networks(networks):
    """
    Gets the posts stored in the database with the given network type.
    """
    return repository.posts.list_posts_on_networks(networks)


def create_ingestion_job(network, content):
    """
    Connects to Redis server and publishes a message to process.
    This might be improved to avoid repeating the connection process.
    """
    red = redis.Redis(redis_url, redis_port, charset="utf-8")
    red.publish(network, json.dumps(content))
