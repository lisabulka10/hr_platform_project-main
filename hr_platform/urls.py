from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="HR-Platform API",
        default_version='v1',
        description="hr_platform application documentation",
    ),
    permission_classes=[],  # откроет доступ в Swagger UI
    public=True
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("resumes.urls")),
    path("api/users/", include("users.urls")),
    path("swagger.<format>/", schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]

