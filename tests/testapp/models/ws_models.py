from django.db import models

from search_categories_core.models import SearchCategoryCore


class WsSearchCategory(SearchCategoryCore):
    """
    Simulates the use of the SearchCategoryCore model in WS.
    """
    sub_category = models.ForeignKey('testapp.WsSearchCategory', null=True, blank=True, on_delete=models.CASCADE)
    product_bases = models.ManyToManyField('testapp.WsProductBase', blank=True)


class WsProductBase(models.Model):
    """
    Simulates the WS Product model.
    """
    pass


class WsProduct(models.Model):
    """
    Simulates the WS Product model.
    """
    pass
