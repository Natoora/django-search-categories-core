from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from .views import SearchCategoryViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'', SearchCategoryViewSet, basename='search-categories')

urlpatterns = [
    url(r'', include(router.urls)),
]
