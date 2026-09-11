from urllib.parse import urlencode, urlparse, urlunparse


def build_url(base_url, path="", args_dict=None):
    parsed_url = urlparse(base_url)
    base_path = parsed_url.path.rstrip("/")
    extra_path = (path or "").lstrip("/")
    final_path = f"{base_path}/{extra_path}" if extra_path else base_path or "/"
    query = urlencode(args_dict or {}, doseq=True)
    final_url = urlunparse(parsed_url._replace(path=final_path, query=query))
    return final_url
