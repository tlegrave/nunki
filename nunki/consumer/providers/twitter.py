import json
import logging
import re
from datetime import datetime

from nunki import models

from . import _helpers

TWITTER_SHORTLINK_REGEX = "https?://t.co/[a-zA-Z\d]{10}"
TWITTER_STATUS_URL = "https://twitter.com/i/web/status/"


def _retrieve_post_url(post):
    """
    Retrieves a twitter post URL either by extracting shortlink from the post text or building it from the post ID.
    """
    if re.search(TWITTER_SHORTLINK_REGEX, post["text"]) is not None:
        return re.search(TWITTER_SHORTLINK_REGEX, post["text"])[0]
    elif post["id_str"] is not None:
        return TWITTER_STATUS_URL + post["id_str"]
    else:
        return ""


def extract_posts(msg: str):
    """
    Takes the response from Twitter API and parses it to extract and normalize all the posts.
    """
    posts = json.loads(msg)

    if "statuses" not in posts or posts["statuses"] is None:
        # Special care should be taken here in real world use cases...
        logging.error("Received data on twitter channel has incorrect format.")
        return []

    extracted_posts = []
    for post in posts["statuses"]:
        try:
            extracted_posts.append(
                models.Post(
                    url=_retrieve_post_url(post),
                    text=_helpers.normalize_unicode_text(post["text"]),
                    publication_date=datetime.strptime(
                        post["created_at"], "%a %b %d %H:%M:%S %z %Y"
                    ),
                    network=models.Network.twitter,
                )
            )
        except Exception as err:
            logging.warn(
                "Twitter post could not be parsed. Err: %s. Post: %s", err, post["text"]
            )
    return extracted_posts


def process_posts(msg: str):
    posts = extract_posts(msg)
    models.bulk_posts_insert(posts)
