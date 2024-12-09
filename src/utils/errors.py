import requests

from utils.auth import get_new_token
from utils.logging_config import logger


def handle_http_error(e, retry_callback, headers):
    """
    Handles HTTP errors, including authentication and automatic retries.

    :param e: Exception caught (typically of type requests.exceptions.HTTPError).
    :param retry_callback: Function to execute for retrying the operation.
    :param headers: The headers dictionary to update with a new token if necessary.
    :raises: Re-raises the exception if it is not manageable.
    """
    if isinstance(e, requests.exceptions.HTTPError) and e.response is not None:
        try:
            error_content = e.response.json()
            logger.error(f"Error content from server: {error_content}")

            if (
                error_content.get("code") == "UnauthorizedError"
                and "expired" in error_content.get("description", "").lower()
            ):
                token = get_new_token()
                headers["Authorization"] = f"Bearer {token}"
                logger.info("Retrying operation with new token.")

                retry_callback()
                return headers

        except ValueError:
            logger.error(
                f"Failed to parse error response as JSON. Response text: {e.response.text}"
            )

    logger.error(f"An unexpected error occurred: {str(e)}")
    raise e
