import logging
import os
import base64
import json

from google.oauth2 import service_account
from storages.backends.gcloud import GoogleCloudStorage

logger = logging.getLogger(__name__)


def get_bucket_name():
    return os.environ.get("SEARCH_CATEGORIES_GCP_BUCKET_NAME", None)


def get_credentials():
    try:
        """Get credentials from a base64 encoded json stored in a env var"""
        gs_creds = os.environ.get("SEARCH_CATEGORIES_GCP_CREDENTIALS", None)
        decoded_to_bytes = base64.b64decode(gs_creds)
        info = decoded_to_bytes.decode("ascii")
        credentials = json.loads(info)
        return service_account.Credentials.from_service_account_info(credentials)
    except Exception as e:
        pass


class GCloudStorage(GoogleCloudStorage):
    """Tiny extension to the GoogleCloudStorage class to allow for class variables to be defined for this app.

    (i.e. not project-wide for WS).
    """

    bucket_name = get_bucket_name()
    credentials = get_credentials()

    def __init__(self, **settings):
        super().__init__(**settings)
