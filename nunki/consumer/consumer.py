import os

import redis

from .providers import PROVIDERS

redis_url = os.getenv("REDIS_URL", "localhost")
redis_port = os.getenv("REDIS_PORT", 6379)

red = redis.Redis(redis_url, redis_port, charset="utf-8", decode_responses=True)


def read_messages(sub):
    """
    Listen for any new message published and assign it to the correct provider for parsing and storing.
    """
    for message in sub.listen():
        if message["type"] == "message":
            if message["channel"] in PROVIDERS:
                PROVIDERS[message["channel"]].process_posts(message["data"])


def start_consumer():
    """
    Starts a consumer.
    """
    sub = red.pubsub()
    sub.subscribe(*PROVIDERS.keys())
    read_messages(sub)
