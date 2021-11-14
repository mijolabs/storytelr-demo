from test_config import Configuration
import json

import httpx


config = Configuration()


def test_get_message():    
    request_body = {
        "message":
            "Let us make the world a more empathetic and creative place "\
            "with great stories to be shared and enjoyed by anyone, anywhere and anytime."
    }
    
    post_message_response = httpx.post(config.base_url, json=request_body, auth=(config.username, config.password))
    post_message_response_json = post_message_response.json()


    get_message_response = httpx.get(post_message_response_json["url"])

    assert get_message_response.status_code == 200
    assert get_message_response.headers["Content-Type"] == "application/json"

    get_message_response_json = get_message_response.json()
    assert get_message_response_json == post_message_response_json
