import json
import logging
from datetime import datetime

from nunki import models

from . import _helpers


def _retrieve_post_url(post):
    return f"https://vk.com/{post['owner_id']}/{post['id']}"


def extract_posts(posts):
    """
    Takes the response from Vkontakte API and parses it to extract and normalize all the posts.
    """
    posts = json.loads(posts)

    if "response" not in posts or "items" not in posts["response"]:
        # Special care should be taken here in real world use cases...
        logging.error("Received data on vkontakte channel has incorrect format.")
        return

    extracted_posts = []

    for post in posts["response"]["items"]:
        try:
            extracted_posts.append(
                models.Post(
                    url=_retrieve_post_url(post),
                    text=_helpers.normalize_unicode_text(post["text"]),
                    publication_date=datetime.fromtimestamp(post["date"]),
                    network=models.Network.vkontakte,
                )
            )
        except Exception as err:
            logging.error(
                "Vkontakte post could not be parsed. Err: %s. Post: %s",
                err,
                post["text"],
            )

    return extracted_posts


def process_posts(msg: str):
    """
    Processes Vkontakte API response to extract, normalize and store posts.
    """
    posts = extract_posts(msg)
    models.bulk_posts_insert(posts)
