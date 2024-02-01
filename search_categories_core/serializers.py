from rest_framework import serializers


class SearchCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the SearchCategory model.
    """

    sub_categories = serializers.SerializerMethodField()

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
            "sub_categories",
        ]
        read_only_fields = fields

    def get_sub_categories(self, instance):
        if hasattr(instance, "sub_categories"):
            return instance.sub_categories.all().filter(products__status="ACTIVE").distinct().values("name", "id")
        else:
            return []
