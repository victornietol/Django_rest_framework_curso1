from rest_framework import generics, viewsets, status
from rest_framework.response import Response

from apps.base.api import GeneralListAPIView
from apps.products.api.serializers.general_serializers import MeasureUnitSerializer, IndicatorSerializer, CategoryProductSerializer

# ListAPIView solo reconoce metodo GET
#class MeasureUnitListAPIView(GeneralListAPIView): # Esta super clase es la principal de django para listar informacion
class MeasureUnitViewSet(viewsets.GenericViewSet):
    '''
    Comentario de documentacion de la clase MeasureUnitViewSet
    '''
    serializer_class = MeasureUnitSerializer
    
    # Esto se necesita si en la clase se hereda de generics.ListAPIView, pero en este caso ya no se coloca debido
    # a que ahora se hereda de la clase personalizada GenerlListAPIView que contiene la fucion get_queryset que cumple la misma funcion
    # Ahora generics.ListAPIView se utiliza en esa clase padre

    # def get_queryset(self):
    #     return MeasureUnit.objects.filter(state=True) # Solo muestra los campos activos
    

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state=True)
    
    def list(self, request):
        '''
        Titulo del comentario

        Comentario de documentacion de funcion 'list()'
        '''
        data = self.get_queryset()
        data = self.get_serializer(data, many=True)
        return Response(data.data)
    
    # Para que Swagger haga la documentacion automaticamente se deben definir (sobreescribir) 
    # los metodos de la clase como list, create, retrieve, destroy, etc. siempre y cuando se utilice 
    # GenericViewSet. En caso de usar ModelViewSet genera automaticamente todos los endpoints 
    # sin necesidad de sobreescribirlos
    def create(self, request):
        return Response({})
    

class IndicatorViewSet(viewsets.GenericViewSet):
    serializer_class = IndicatorSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state=True)
    
    def list(self, request):
        '''
        Titulo del comentario

        Comentario de documentacion de funcion 'list()'
        '''
        data = self.get_queryset()
        data = self.get_serializer(data, many=True)
        return Response(data.data)

    def create(self, request):
        return Response({})
    

class CategoryProductViewSet(viewsets.GenericViewSet):
    serializer_class = CategoryProductSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state=True)
    
    def get_object(self): # Obtener el objeto con el id correspondiente
        return self.get_serializer().Meta.model.objects.filter(id=self.kwargs["pk"], state=True)

    def list(self, request):
        '''
        Titulo del comentario

        Comentario de documentacion de funcion 'list()'
        '''
        data = self.get_queryset()
        data = self.get_serializer(data, many=True)
        return Response(data.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Categoria registrada correctamente."}, status=status.HTTP_201_CREATED)
        return Response({"message":"", "error":serializer.error}, status=status.HTTP_400_BAD_REQUEST)

    # Actualizar categoria producto
    def update(self, request, pk=None):
        if self.get_object().exists():
            serializer = self.serializer_class(instance=self.get_object().get(), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"Categoria actualizada correctamente."}, status=status.HTTP_200_OK)
        return Reponse({"message":"", "error":serializer.error}, status=status.HTTP_400_BAD_REQUEST)
    
    # Eliminar
    def destroy(self, request, pk=None):
        query = self.get_object()
        if query.exists():
            category = query.get()
            category.state = False # ELIMINACIO LOGICA (es lo mismo que 'self.get_object().get().state' pero en partes)
            category.save()
            # self.get_object().get().delete() # ELIMINACIO COMPLETA
            return Response({"message":"Categoria eliminada correctamente."}, status=status.HTTP_200_OK)
        return Response({"message":"", "error":"Categoria no encontrada."}, status=status.HTTP_400_BAD_REQUEST)