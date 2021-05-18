from django.test import TestCase

from search_categories_core.services import SearchCategorySyncService
from tests.factories import get_or_create_ws_search_category
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

    @staticmethod
    def run_sync():
        sync_service = SearchCategorySyncService(
            WsProduct=WsProduct,
            WsCategory=WsSearchCategory,
            AppProduct=AppProduct,
            AppCategory=AppSearchCategory,
            image_scp_destination="/tmp/image_destination"
        )
        sync_service.sync()

    def test_sync_service(self):
        """
        Create a WS Search Category, run the sync service,
        get the app search category and compare the names.
        """
        ws_sc = get_or_create_ws_search_category()
        self.run_sync()
        app_sc = AppSearchCategory.objects.get(code=ws_sc.code)
        self.assertEqual(ws_sc.name, app_sc.name)
