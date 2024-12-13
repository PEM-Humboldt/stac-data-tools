import requests

from utils.auth import authenticate
from config import get_settings


def get_headers():
    """
    Generate Authorization header dynamically using the current token.
    """
    settings = get_settings()
    return {"Authorization": f"Bearer {settings.token}"}


def post_or_put(url: str, data: dict):
    """
    Post or put data to URL
    """

    try:
        headers = get_headers()
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 401:
            if (
                response.json().get("code") == "UnauthorizedError"
                and "expired" in response.json().get("description", "").lower()
            ):
                authenticate()
                headers = get_headers()
                response = requests.post(url, json=data, headers=headers)

        if response.status_code == 409:
            response = requests.put(url, json=data, headers=headers)

        response.raise_for_status()

        return response
    except requests.exceptions.RequestException as e:
        raise e


def get(url: str):
    """
    Get request
    """
    response = requests.get(url)
    response.raise_for_status()
    return response


def check_resource(url: str):
    """
    Check if an URL for a resource exists. e.g. items, collections, catalogues
    """
    response = requests.get(url)
    if response.status_code == 200:
        success = True
    elif response.status_code == 404:
        success = False
    else:
        response.raise_for_status()
    return success


def delete(url):
    """
    Delete request
    """
    headers = get_headers()
    response = requests.delete(url, headers=headers)
    if response.status_code == 401:
        if (
            response.json().get("code") == "UnauthorizedError"
            and "expired" in response.json().get("description", "").lower()
        ):
            authenticate()
            headers = get_headers()
            response = requests.delete(url, headers=headers)
            if response.status_code == 200:
                success = True
            elif response.status_code == 404:
                success = False
            else:
                response.raise_for_status()
    elif response.status_code == 200:
        success = True
    elif response.status_code == 404:
        success = False

    else:
        response.raise_for_status()
    return success
