from django.db import models

from search_categories_core.models import SearchCategoryCore


class AppSearchCategory(SearchCategoryCore):
    """
    Simulates the use of the SearchCategoryCore model in an app backend.
    """
    pass


class AppProduct(models.Model):
    """
    Simulates an app Product model.
    """
    pass
