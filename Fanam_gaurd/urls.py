from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    # 🔹 Admin UI
    path('admin/', admin.site.urls),

    # 🔹 Business Users API
    path('business/', include('bussiness_user.urls')),

    # 🔹 Guest Users API
    path('guest/', include('guest_user.urls')),

    # 🔹 OpenAPI schema
    path('schema/', SpectacularAPIView.as_view(), name='schema'),

    # 🔹 Swagger UI
    path(
        'swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),

    # 🔹 ReDoc UI
    path(
        'redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
]

# ✅ REQUIRED: serve audio files locally
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
