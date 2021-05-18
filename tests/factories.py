from django.utils import timezone as tz

from tests.testapp.models import WsSearchCategory


def get_or_create_ws_search_category():
    ws_sc = WsSearchCategory()
    ws_sc.created_at = tz.now()
    ws_sc.updated_at = tz.now()
    ws_sc.name = "Fruit"
    ws_sc.code = "LDN587"
    ws_sc.save()
    return ws_sc
