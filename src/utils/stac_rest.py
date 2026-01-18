import requests

from config import get_settings
from utils.auth import authenticate


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
        import json

        headers = get_headers()
        headers["Content-Type"] = "application/json; charset=utf-8"
        response = requests.post(
            url,
            data=json.dumps(data, ensure_ascii=False).encode("utf-8"),
            headers=headers,
        )

        if response.status_code == 401:
            if (
                response.json().get("code") == "UnauthorizedError"
                and "expired" in response.json().get("description", "").lower()
            ):
                authenticate()
                headers = get_headers()
                headers["Content-Type"] = "application/json; charset=utf-8"
                response = requests.post(
                    url,
                    data=json.dumps(data, ensure_ascii=False).encode("utf-8"),
                    headers=headers,
                )

        if response.status_code == 409:
            headers["Content-Type"] = "application/json; charset=utf-8"
            response = requests.put(
                url,
                data=json.dumps(data, ensure_ascii=False).encode("utf-8"),
                headers=headers,
            )

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
        success = False
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
                success = False
        else:
            response.raise_for_status()
            success = False
    elif response.status_code == 200:
        success = True
    elif response.status_code == 404:
        success = False
    else:
        response.raise_for_status()
        success = False
    return success
