from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("usuario/", include("apps.users.api.urls")),
    # path("products/", include("apps.products.api.urls")), # Este enlaza las funciones individuales para manejar las peticiones
    path("products/", include("apps.products.api.routers")), # Este enlaza el router para ModelViewSet
]
