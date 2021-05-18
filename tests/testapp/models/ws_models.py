from django.db import models

from search_categories_core.models import SearchCategoryCore


class WsSearchCategory(SearchCategoryCore):
    """
    Simulates the use of the SearchCategoryCore model in WS.
    """
    pass


class WsProduct(models.Model):
    """
    Simulates the WS Product model.
    """
    pass
