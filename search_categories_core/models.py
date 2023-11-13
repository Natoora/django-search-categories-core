import os

from django.db import models
from django.db.models import Q
from django.utils import timezone as tz

from .gcloud_storage import GCloudStorage

image_cdn_location = os.environ.get("SEARCH_CATEGORY_IMAGE_CDN_LOCATION", "search_categories/images")


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

    HD = "HD"
    PRO = "PRO"
    APP_CHOICES = [
        (HD, 'HD'),
        (PRO, 'PRO')
    ]

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=20, editable=False, unique=True)
    hierarchy = models.IntegerField(default=1, null=True, blank=True)
    background_image = models.ImageField(upload_to='products/search_categories/')
    image_cdn = models.ImageField(
        upload_to=image_cdn_location,
        null=True,
        blank=True,
        storage=GCloudStorage(),
        help_text="Google Cloud Stored product image.",
    )
    image_blurred_hash = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Hash to store blurred version of image_cdn",
    )
    tile_dimensions = models.CharField(max_length=50, choices=DIMENSION_CHOICES, default=FULL_WIDTH)
    enabled = models.BooleanField(default=False)
    app_type = models.CharField(max_length=50, choices=APP_CHOICES, default=HD)
    synchronised = models.BooleanField(
        default=False,
        editable=False,
        help_text="Synchronised with the app"
    )
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "app_type"],
                condition=Q(deleted=False),
                name="name_app_type_unique_if_not_deleted")
        ]
        verbose_name = "Search Category"
        verbose_name_plural = "Search Categories"
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Override model save() method to update updated and created at.
        """
        self.synchronised = False
        self.updated_at = tz.localtime()
        if not self.pk:
            self.created_at = tz.localtime()
        update_image_blurred_hash(self)
        super(SearchCategoryCore, self).save(*args, **kwargs)
