from django.urls import path

from apps.products.api.views.general_views import MeasureUnitViewSet, IndicatorViewSet, CategoryProductViewSet
from apps.products.api.views.product_views import (
    ProductListAPIView, ProductCreateAPIView, ProductRetrieveAPIView, ProductDestroyAPIView,
    ProductUpdateAPIView, ProductListCreateAPIView, ProductRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path("measure_unit/", MeasureUnitViewSet.as_view(), name="measure_unit"),
    path("indicator/", IndicatorViewSet.as_view(), name="indicator"),
    path("category_product/", CategoryProductViewSet.as_view(), name="category_product"),

    path("product/", ProductListCreateAPIView.as_view(), name="product"), # Combina e lfuncionamiento de las dos urls siguientes
    #path("product/list/", ProductListAPIView.as_view(), name="product_list"),
    #path("product/create/", ProductCreateAPIView.as_view(), name="product_create"),


    path("product/retrieve-update-destroy/<int:pk>/", ProductRetrieveUpdateDestroyAPIView.as_view(), name="product_retrieve"), # Combina el funcionamiento de Retrieve y Update delas 2 sig urls
    #path("product/retrieve/<int:pk>/", ProductRetrieveAPIView.as_view(), name="product_retrieve"),
    #path("product/update/<int:pk>/", ProductUpdateAPIView.as_view(), name="product_update"),
    #path("product/destroy/<int:pk>/", ProductDestroyAPIView.as_view(), name="product_destroy"),
]