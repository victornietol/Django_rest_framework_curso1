from django.contrib import admin
from django.urls import path, include

# Importaciones para la auto documentacion drf-yasg
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Autenticacion de usuarios
from apps.users.views import Login, Logout, UserToken

# Necesario para drf-yasg
schema_view = get_schema_view(
    openapi.Info(
        title="Documentacion API",
        default_version='v0.1',
        description="Documentacion publica de API de Ecommerce",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Urls de drf-yasg
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Auth de usuarios
    path("", Login.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
    path("refresh-token/", UserToken.as_view(), name="refresh_token"), # Vista para refrescar token

    path("admin/", admin.site.urls),
    path("usuario/", include("apps.users.api.urls")),
    # path("products/", include("apps.products.api.urls")), # Este enlaza las funciones individuales para manejar las peticiones
    path("products/", include("apps.products.api.routers")), # Este enlaza el router para ModelViewSet
]
