from rest_framework.serializers import ModelSerializer

from .models import SearchCategoryCore


class SearchCategorySerializer(ModelSerializer):
    """
    Serializer for the SearchCategory model.
    """

    class Meta:
        model = SearchCategoryCore
        fields = [
            "id",
            "name",
            "enabled",
            "background_image",
            "tile_dimensions"
        ]
        read_only_fields = fields
