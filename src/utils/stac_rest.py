import requests


def post_or_put(url: str, data: dict):
    """
    Post or put data to url
    """

    response = requests.post(url, json=data)
    if response.status_code == 409:
        response = requests.put(url, json=data)
        if not response.status_code == 404:
            response.raise_for_status()
    else:
        response.raise_for_status()


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
