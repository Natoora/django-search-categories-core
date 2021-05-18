import os

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

    def test_name_field(self):
        fifty_char_string = "".join(["a" for _ in range(50)])
        sc = WsSearchCategory.objects.create(name=fifty_char_string)
        self.assertEquals(
            sc.name,
            fifty_char_string
        )

    def test_code_field(self):
        twenty_char_string = "".join(["a" for _ in range(20)])
        sc = WsSearchCategory.objects.create(code=twenty_char_string)
        self.assertEquals(
            sc.code,
            twenty_char_string
        )

    def test_hierarchy_field(self):
        sc = WsSearchCategory.objects.create()
        self.assertEquals(
            sc.hierarchy,
            1
        )

    def test_enabled_field(self):
        sc = WsSearchCategory.objects.create()
        self.assertEquals(
            sc.enabled,
            True
        )

    def test_background_image_field(self):
        img_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'misc', 'test_image.png'
        )
        sc = WsSearchCategory.objects.create()
        with open(img_path, 'rb') as img:
            sc.background_image.save('test_image.png', content=img)
        self.assertIn(
            "test_image",
            sc.background_image.url
        )

    def test_tile_dimensions_field(self):
        sc = WsSearchCategory.objects.create()
        self.assertEquals(
            sc.tile_dimensions,
            sc.FULL_WIDTH
        )

    def test_synchronised_field(self):
        sc = WsSearchCategory.objects.create()
        self.assertFalse(sc.synchronised)
