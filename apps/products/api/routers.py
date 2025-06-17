# Manejar las rutas de los ModelViewSet
from rest_framework.routers import DefaultRouter
from apps.products.api.views.product_views import ProductViewSet

router = DefaultRouter()

router.register(r"products", ProductViewSet, basename="products")

urlpatterns = router.urls
