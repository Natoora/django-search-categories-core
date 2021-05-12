from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from .models import SearchCategoryCore
from .serializers import SearchCategorySerializer


class SearchCategoryViewSet(ModelViewSet):
    """
    ViewSet for the SearchCategory model.
    """
    permission_classes = (AllowAny,)
    serializer_class = SearchCategorySerializer
    queryset = SearchCategoryCore.objects.filter(enabled=True)
