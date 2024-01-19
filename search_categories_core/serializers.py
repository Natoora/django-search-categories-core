from rest_framework import serializers


class SearchCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the SearchCategory model.
    """

    class Meta:
        abstract = True
        fields = [
            "id",
            "created_at",
            "updated_at",
            "name",
            "code",
            "hierarchy",
            "background_image",
            "image_cdn",
            "image_blurred_hash",
            "tile_dimensions",
            "enabled",
            "app_type",
            "synchronised",
            "products",
            "deleted",
        ]
        read_only_fields = fields
