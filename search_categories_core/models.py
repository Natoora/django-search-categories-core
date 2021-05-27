from django.db import models
from django.utils import timezone as tz


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
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=20, editable=False, unique=True)
    hierarchy = models.IntegerField(default=1)
    background_image = models.ImageField(upload_to='products/search_categories/')
    tile_dimensions = models.CharField(max_length=50, choices=DIMENSION_CHOICES, default=FULL_WIDTH)
    hd_app = models.BooleanField(default=False, help_text="Category will appear on the HD app")
    pro_app = models.BooleanField(default=False, help_text="Category will appear on the Pro app")
    hd_synchronised = models.BooleanField(
        default=False,
        editable=False,
        help_text="Synchronised with the HD app"
    )
    pro_synchronised = models.BooleanField(
        default=False,
        editable=False,
        help_text="Synchronised with the Pro app"
    )

    class Meta:
        verbose_name = "Search Category"
        verbose_name_plural = "Search Categories"
        ordering = ["hierarchy"]
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Override model save() method to update updated and created at.
        """
        self.hd_synchronised = False
        self.pro_synchronised = False
        self.updated_at = tz.localtime()
        if not self.pk:
            self.created_at = tz.localtime()
        super(SearchCategoryCore, self).save(*args, **kwargs)
