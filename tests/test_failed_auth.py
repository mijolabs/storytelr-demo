from test_config import Configuration
import json

import httpx


config = Configuration()


def test_failed_auth():    
    request_body = {
        "message":
            "Let us make the world a more empathetic and creative place "\
            "with great stories to be shared and enjoyed by anyone, anywhere and anytime."
    }
    
    incorrect_username = "incorrect_username"
    incorrect_password = "incorrect_password"
    
    # Test incorrect username
    post_message_response = httpx.post(config.base_url, json=request_body, auth=(incorrect_username, config.password))
    assert post_message_response.status_code == 401
    assert post_message_response.headers["Content-Type"] == "application/json"

    # Test incorrect password
    post_message_response = httpx.post(config.base_url, json=request_body, auth=(config.username, incorrect_password))
    assert post_message_response.status_code == 401
    assert post_message_response.headers["Content-Type"] == "application/json"

    # Test incorrect username and password
    post_message_response = httpx.post(config.base_url, json=request_body, auth=(incorrect_username, incorrect_password))
    assert post_message_response.status_code == 401
    assert post_message_response.headers["Content-Type"] == "application/json"
