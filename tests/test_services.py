from django.test import TestCase

from search_categories_core.services import SearchCategorySyncService
from tests.testapp.models import (
    WsSearchCategory,
    WsProduct,
    AppSearchCategory,
    AppProduct
)


class SyncServiceTestCase(TestCase):
    """
    Tests for the sync service.
    """

    def test_sync_service(self):
        sync_service = SearchCategorySyncService(
            WsProduct=WsProduct,
            WsCategory=WsSearchCategory,
            AppProduct=AppProduct,
            AppCategory=AppSearchCategory,
            image_scp_destination="/tmp/image_destination"
        )
        sync_service.sync()
