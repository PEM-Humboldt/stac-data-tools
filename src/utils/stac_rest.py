import requests

from utils.auth import authenticate, settings


def post_or_put(url: str, data: dict, headers: dict = None):
    """
    Post or put data to URL
    """
    try:
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 409:
            response = requests.put(url, json=data, headers=headers)

        if response.status_code == 401:
            if (
                response.json().get("code") == "UnauthorizedError"
                and "expired" in response.json().get("description", "").lower()
            ):
                authenticate()
                headers["Authorization"] = f"Bearer {settings.token}"
                response = requests.post(url, json=data, headers=headers)

        response.raise_for_status()

        return response
    except requests.exceptions.RequestException as e:
        raise e


def get(url: str):
    """
    Get request
    """
    response = requests.get(
        url,
    )
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


def delete(url, headers: dict = None):
    """
    Delete request
    """
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        success = True
    elif response.status_code == 404:
        success = False
    elif response.status_code == 401:
        if (
            response.json().get("code") == "UnauthorizedError"
            and "expired" in response.json().get("description", "").lower()
        ):
            authenticate()
            headers["Authorization"] = f"Bearer {settings.token}"
            response = requests.delete(url, headers=headers)
            if response.status_code == 200:
                success = True
            elif response.status_code == 404:
                success = False
            else:
                response.raise_for_status()
    else:
        response.raise_for_status()
    return success
