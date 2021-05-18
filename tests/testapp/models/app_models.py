from django.db import models

from search_categories_core.models import SearchCategoryCore


class AppSearchCategory(SearchCategoryCore):
    """
    Simulates the use of the SearchCategoryCore model in an app backend.
    """
    sub_category = models.ForeignKey(
        'testapp.AppSearchCategory',
        null=True, blank=True,
        on_delete=models.CASCADE
    )
    products = models.ManyToManyField('testapp.AppProduct', blank=True)


class AppProduct(models.Model):
    """
    Simulates an app Product model.
    """
    pass
