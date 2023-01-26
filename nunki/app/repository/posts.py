from sqlalchemy import or_

from nunki import models


def list_posts_on_networks(networks):
    """
    Gets posts stored in the database and return them as a list on dict with url, date, text and network.
    """
    with models.Session.begin() as session:
        or_clause = or_(*((models.Post.network == net) for net in networks))
        posts = session.query(models.Post).filter(or_clause).all()

        return [
            {
                "url": post.url,
                "date": post.publication_date,
                "text": post.text,
                "network": post.network.name,
            }
            for post in posts
        ]
