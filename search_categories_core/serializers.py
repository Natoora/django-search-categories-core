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
            "background_image",
            "tile_dimensions",
            "hd_app",
            "pro_app",
            "hd_synchronised",
            "pro_synchronised",
        ]
        read_only_fields = fields
