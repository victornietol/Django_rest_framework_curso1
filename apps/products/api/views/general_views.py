from rest_framework import generics

from apps.products.models import MeasureUnit, Indicator, CategoryProduct
from apps.products.api.serializers.general_serializers import MeasureUnitSerializer, IndicatorSerializer, CategoryProductSerializer

# ListAPIView solo reconoce metodo GET
class MeasureUnitListAPIView(generics.ListAPIView): # Esta super clase es la principal de django para listar informacion
    serializer_class = MeasureUnitSerializer
    
    def get_queryset(self):
        return MeasureUnit.objects.filter(state=True) # Solo muestra los campos activos
    

class IndicatorListAPIView(generics.ListAPIView):
    serializer_class = IndicatorSerializer
    
    def get_queryset(self):
        return Indicator.objects.filter(state=True)
    

class CategoryProductListAPIView(generics.ListAPIView):
    serializer_class = CategoryProductSerializer
    
    def get_queryset(self):
        return CategoryProduct.objects.filter(state=True)