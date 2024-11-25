import requests
from utils.logging_config import logger
from sys import exit as sysexit


def authenticate(username, password, stac_url, auth_url):
    """
    Authenticate against the authentication service and retrieve a token.
    """
    try:
        auth_data = {
            "username": username,
            "password": password
        }

        response = requests.post(
            f"{stac_url}{auth_url}", data=auth_data
        )
        response.raise_for_status()  # Lanza un error si la respuesta tiene un código de error HTTP

        token = response.json().get("access_token")

        if not token:
            logger.error("Authentication failed: No token received.")
            sysexit("Authentication failed: No token received.")

        return token



    except requests.HTTPError as http_err:
        error_detail = None

        status_code = response.status_code if response is not None else "Unknown"

        if response is not None and response.headers.get('Content-Type') == 'application/json':

            try:
                error_detail = response.json().get("detail", str(http_err))

            except ValueError:

                error_detail = str(http_err)

        error_message = f"HTTP {status_code}: {error_detail or str(http_err)}"

        sysexit(f"Authentication error: {error_message}")


    except requests.RequestException as req_err:
        sysexit(f"Request error: {req_err}")
