from django.db import models
from django.utils import timezone as tz

# from django.conf import settings
from .services import update_image_blurred_hash

# DynamicGoogleCloudStorage = getattr(settings, "APP_DEFAULT_STORAGE", None)


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
    background_image = models.ImageField(
        upload_to="images/search_categories",
        null=True,
        blank=True,
        # storage=DynamicGoogleCloudStorage(default_acl="publicRead"),
        help_text="Google Cloud Stored product image.",
    )
    # TODO: remove this field, serializer takes care of backwards compatability
    image_cdn = models.ImageField(
        upload_to="images/search_categories",
        null=True,
        blank=True,
        # storage=DynamicGoogleCloudStorage(default_acl="publicRead"),
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
