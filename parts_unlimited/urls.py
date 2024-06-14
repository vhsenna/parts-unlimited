from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from parts.views import PartViewSet

router = routers.DefaultRouter()
router.register(r"parts", PartViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Parts Unlimited API",
        default_version='v1',
        description="",
        contact=openapi.Contact(email="vhsenna@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("parts.urls")),
    path("swagger/", schema_view.with_ui("swagger",
         cache_timeout=0)),
    path("docs/", schema_view.with_ui("redoc",
         cache_timeout=0)),
]
