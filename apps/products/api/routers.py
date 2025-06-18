# Manejar las rutas de los ModelViewSet
from rest_framework.routers import DefaultRouter

from apps.products.api.views.product_views import ProductViewSet
from apps.products.api.views.general_views import *


router = DefaultRouter()

router.register(r"products", ProductViewSet, basename="products")
router.register(r"measure-unit", MeasureUnitViewSet, basename="measure_unit")
router.register(r"indicators", IndicatorViewSet, basename="indicators")
router.register(r"category-products", CategoryProductViewSet, basename="category_products")

urlpatterns = router.urls
