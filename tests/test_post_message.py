from test_config import Configuration
import json
from urllib.parse import urlparse

import httpx


config = Configuration()


def test_post_message():
    """
    Test for creating a new message
    """
    request_body = {
        "message":
            "Let us make the world a more empathetic and creative place "\
            "with great stories to be shared and enjoyed by anyone, anywhere and anytime."
    }
    
    # Create a new message
    post_message_response = httpx.post(config.base_url, json=request_body, auth=(config.username, config.password))
    
    assert post_message_response.status_code == 201
    assert post_message_response.headers["Content-Type"] == "application/json"

    post_message_response_json = post_message_response.json()
    assert post_message_response_json["message"] == request_body["message"]
    assert type(post_message_response_json["created"]) == int
    assert type(post_message_response_json["expires"]) == int

    response_url_value = urlparse(post_message_response_json["url"])
    assert "http" in response_url_value.scheme
    assert len(response_url_value.netloc) > 0
