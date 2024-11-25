import requests

def post_or_put(url: str, data: dict,headers: dict = None):
    """
    Post or put data to URL
    """
    try:
        response = requests.post(url, json=data,headers=headers)

        # Si el POST falla con 409, intenta con PUT
        if response.status_code == 409:
            response = requests.put(url, json=data,headers=headers)

        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error during post or put: {e}")
        raise e


def get(url: str,headers: dict = None):
    """
    Get request
    """
    response = requests.get(url, headers=headers)
    print(response)
    response.raise_for_status()
    return response


def check_resource(url: str,headers: dict = None):
    """
    Check if an URL for a resource exists. e.g. items, collections, catalogues
    """
    response = requests.get(url,headers=headers)
    print(response)
    if response.status_code == 200:
        success = True
    elif response.status_code == 404:
        success = False
    else:
        response.raise_for_status()
    return success


def delete(url,headers: dict = None):
    """
    Delete request
    """
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        success = True
    elif response.status_code == 404:
        success = False
    else:
        response.raise_for_status()
    return success
