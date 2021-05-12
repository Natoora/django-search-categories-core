from django.db import models


class SearchCategoryCore(models.Model):
    """
    Category of products to search.
    """
    FULL_WIDTH = "FULL_WIDTH"
    HALF_WIDTH = "HALF_WIDTH"
    DIMENSION_CHOICES = [
        (FULL_WIDTH, "Full Width"),
        (HALF_WIDTH, "Half Width"),
    ]
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=20, editable=False, unique=True)
    hierarchy = models.IntegerField(default=1)
    enabled = models.BooleanField(default=True)
    background_image = models.ImageField(upload_to='products/search_categories/')
    tile_dimensions = models.CharField(max_length=50, choices=DIMENSION_CHOICES, default=FULL_WIDTH)
    synchronised = models.BooleanField(default=False, help_text="Synchronised with the app")

    class Meta:
        verbose_name = "Search Category"
        verbose_name_plural = "Search Categories"
        ordering = ["hierarchy"]
        abstract = True

    def __str__(self):
        return self.name
