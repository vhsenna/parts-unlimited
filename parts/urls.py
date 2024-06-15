from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PartViewSet, most_common_words

router = DefaultRouter()
router.register(r"parts", PartViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("most-common-words/", most_common_words, name="most-common-words"),
]
