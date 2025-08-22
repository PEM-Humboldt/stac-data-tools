from sys import exit as sysexit

import requests

from config import get_settings
from utils.logging_config import logger
from utils.url import build_url

settings = get_settings()


def authenticate():
    """
    Authenticate against the authentication service and retrieve a token.
    """
    try:
        username = settings.username_auth
        password = settings.password_auth
        stac_url = settings.stac_url
        auth_url = settings.auth_url

        auth_data = {"username": username, "password": password}

        url = build_url(stac_url, auth_url, args_dict={})
        response = requests.post(url, data=auth_data)
        response.raise_for_status()

        new_token = response.json().get("access_token")

        if new_token:
            settings.set_token(new_token)
            logger.info("Token updated successfully.")
        else:
            logger.error("Authentication failed: No token received.")
            sysexit("Authentication failed: No token received.")

    except requests.HTTPError as http_err:
        error_detail = None

        status_code = (
            response.status_code if response is not None else "Unknown"
        )

        if (
            response is not None
            and response.headers.get("Content-Type") == "application/json"
        ):
            try:
                error_response = response.json()
                error_detail = error_response.get("description", str(http_err))

            except ValueError:
                error_detail = str(http_err)

        error_message = f"HTTP {status_code}: {error_detail or str(http_err)}"
        sysexit(f"Authentication error: {error_message}")

    except requests.RequestException as req_err:
        sysexit(f"Request error: {req_err}")
