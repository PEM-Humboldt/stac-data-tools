from urllib.parse import urlencode, urlparse, urlunparse


def build_url(base_url, path=None, args_dict={}):
    url_parts = list(urlparse(base_url))
    url_parts[2] = path
    url_parts[4] = urlencode(args_dict)
    return urlunparse(url_parts)
