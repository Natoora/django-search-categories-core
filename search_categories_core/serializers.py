from rest_framework.serializers import ModelSerializer


class SearchCategorySerializer(ModelSerializer):
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
            "hierarchy_hd",
            "hierarchy_pro",
            "background_image",
            "tile_dimensions",
            "enabled",
            "app_type",
            "synchronised"
        ]
        read_only_fields = fields
