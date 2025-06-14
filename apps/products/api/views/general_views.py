from rest_framework import generics

from apps.base.api import GeneralListAPIView
from apps.products.api.serializers.general_serializers import MeasureUnitSerializer, IndicatorSerializer, CategoryProductSerializer

# ListAPIView solo reconoce metodo GET
class MeasureUnitListAPIView(GeneralListAPIView): # Esta super clase es la principal de django para listar informacion
    serializer_class = MeasureUnitSerializer
    
    # Esto se necesita si en la clase se hereda de generics.ListAPIView, pero en este caso ya no se coloca debido
    # a que ahora se hereda de la clase personalizada GenerlListAPIView que contiene la fucion get_queryset que cumple la misma funcion
    # Ahora generics.ListAPIView se utiliza en esa clase padre
    '''
    def get_queryset(self):
        return MeasureUnit.objects.filter(state=True) # Solo muestra los campos activos
    '''
    

class IndicatorListAPIView(GeneralListAPIView):
    serializer_class = IndicatorSerializer
    

class CategoryProductListAPIView(GeneralListAPIView):
    serializer_class = CategoryProductSerializer
