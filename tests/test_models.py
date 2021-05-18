from django.test import TestCase
from django.utils import timezone as tz

from tests.testapp.models.ws_models import WsSearchCategory


class SearchCategoryCoreModelTestCase(TestCase):
    """
    Tests for the SearchCategoryCore fields.
    """

    def test_created_at_field(self):
        sc = WsSearchCategory.objects.create()
        now = tz.localtime().strftime("%H:%M")
        self.assertEquals(
            sc.created_at.strftime("%H:%M"),
            now
        )

    def test_updated_at_field(self):
        sc = WsSearchCategory.objects.create()
        now = tz.localtime().strftime("%H:%M")
        self.assertEquals(
            sc.updated_at.strftime("%H:%M"),
            now
        )
