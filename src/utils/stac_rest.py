import requests

from utils.logging_config import logger


def post_or_put(url: str, data: dict):
    """
    Post or put data to url
    """
    try:
        response = requests.post(url, json=data)

        if response.status_code == 409:
            response = requests.put(url, json=data)

        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during post or put: {e}")
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
    response = requests.delete(url)
    if response.status_code == 200:
        success = True
    elif response.status_code == 404:
        success = False
    else:
        response.raise_for_status()
    return success
