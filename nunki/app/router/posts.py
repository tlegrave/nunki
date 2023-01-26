from flask import Blueprint, abort, jsonify, request

from .. import services

posts = Blueprint(
    "posts",
    __name__,
    url_prefix="/",
)


@posts.route("/", methods=["GET"])
def get_posts():
    """
    List all stored posts for the given networks.
    """
    networks = request.args.getlist("network")
    try:
        posts = services.posts.list_posts_on_networks(networks)
    except Exception:  # This try catch is too wide, should focus specific exceptions to have a proper API response.
        abort(500)
    return jsonify(posts)


@posts.route("/", methods=["POST"])
def ingest_posts():
    """
    Creates an ingestion job for the given network.
    """
    network = request.args.get("network")
    content = request.json
    if network is None or content is None:
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Your request should specify a network in its parameters and have a JSON body.",
                }
            ),
            422,
            {"Content-Type": "application/json"},
        )
    try:
        services.posts.create_ingestion_job(network, content)
    except Exception:  # This try catch is too wide, should focus specific exceptions to have a proper API response.
        abort(500)
    return jsonify({"success": True}), 200, {"Content-Type": "application/json"}
