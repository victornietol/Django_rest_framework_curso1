from rest_framework import generics, viewsets
from rest_framework import status
from rest_framework.response import Response

from apps.base.api import GeneralListAPIView
from apps.products.api.serializers.product_serializers import ProductSerializer


# Utilizacion de ViewSets, para usarlo en urls se debe manejar a traves de Router()
# Con ModelViewSet se puede modificar ahora list(), retrieve(), etc. para manejar las peticiones GET, PUT, POST, etc.
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    #queryset = ProductSerializer.Meta.model.objects.filter(state=True) # Si no se define get_queryset

    # Si se sobreescriben los metodos se necesita get_queryset
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state=True)
        return self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()
        
    def list(self, request):
        product_serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(product_serializer.data, status=status.HTTP_200_OK)

    # Manejo manual de la peticion POST
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Producto creado correctamente"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Actualizar
    def update(self, request, pk=None):
        product = self.get_queryset(pk)
        if product:
            product_serializer = self.serializer_class(product, data=request.data)
            if product_serializer.is_valid():
                product_serializer.save()
                return Response(product_serializer.data, status=status.HTTP_200_OK)
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # Definir manualmente lo que hace DELETE, en este caso es un eliminacion logica
    def destroy(self, request, pk=None):
        product = self.get_queryset().filter(id=pk).first()
        if product:
            product.state = False
            product.save()
            return Response(
                {"message": "Producto eliminado correctamemte."},
                status=status.HTTP_200_OK
            )
        return Response({"error":"No existe un producto con esos datos"},status=status.HTTP_400_BAD_REQUEST)

    '''
    # Se pueden sobreescribir varios metodos, entre los cuales:
    def list(self, request): # Peticiones GET
        pass

    def create(self, request): # Peticiones POST
        pass

    def retrieve(self, request, pk=None): # Peticiones GET con un elemento (necesita pk por ejemplo)
        pass

    def update(self, request, pk=None): # PUT
        pass

    def partial_update(self, request, pk=None): # PATCH
        pass

    def destroy(self, request, pk=None): # DELETE
        pass
    '''




# UTILIZACION DE CLASES Y METODOS ESPECIFICOS PARA CONTROLAR LAS PETICIONES
class ProductListAPIView(GeneralListAPIView):
    serializer_class = ProductSerializer

# Si se usa generics.ListCreateAPIView entonces se debe definor 'queryset' o 'def get_queryset' con
# la logica para la consulta. En el siguiente caso se utilizo solo generics.CreateAPIView
# ListCreateAPIView maneja peticiones GET y POST, mientras que ListAPIView solo GET y CreateAPIView solo POST
class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductSerializer

    # Manejo manual de la peticion POST
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Producto creado correctamente"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Recibe GET y POST, combina el funcionamiento de las dos funciones anteriores
class ProductListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = ProductSerializer.Meta.model.objects.filter(state=True)

    # Manejo manual de la peticion POST
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Producto creado correctamente"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



# Hace lo mismo que ProductRetrieveAPIView, ProductUpdateAPIView y ProductDestroyAPIView, es decir 
# maneja peticiones para mostrar solo un elemento, actualizar y eliminar un elemento
# Tambien se le puede sobreescribir el funcionamiento de funciones para get, put, delete
class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state=True)
        else:
            return self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()
    
    # Aqui ahora PATCH me va solo a devolver el objeto, ya no lo actualiza
    def patch(self, request, pk=None):
        product = self.get_queryset(pk)
        if product:
            product_serializer = self.serializer_class(product)
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        return Response({"error":"No existe un producto con esos datos"},status=status.HTTP_400_BAD_REQUEST)

    # Personalizar el funcionamiento de PUT
    def put(self, request, pk=None):
        product = self.get_queryset(pk)
        if product:
            product_serializer = self.serializer_class(product, data=request.data)
            if product_serializer.is_valid():
                product_serializer.save()
                return Response(product_serializer.data, status=status.HTTP_200_OK)
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Definir manualmente lo que hace DELETE, en este caso es un eliminacion logica
    def delete(self, request, pk=None):
        product = self.get_queryset().filter(id=pk).first()
        if product:
            product.state = False
            product.save()
            return Response(
                {"message": "Producto eliminado correctamemte."},
                status=status.HTTP_200_OK
            )
        return Response({"error":"No existe un producto con esos datos"},status=status.HTTP_400_BAD_REQUEST)

# *Estas 3 siguientes clases hacen individualmente lo de la anterior

# Obtener solo un elemento en lugar de una lista
class ProductRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state=True)
    
# Eliminar un elemento, lo manda a llamar el metodo DELETE
class ProductDestroyAPIView(generics.DestroyAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self): # Necesario para filtrar elemento
        return self.get_serializer().Meta.model.objects.filter(state=True)
    
    # Definir manualmente lo que hace DELETE, en este caso es un eliminacion logica
    def delete(self, request, pk=None):
        product = self.get_queryset().filter(id=pk).first()
        if product:
            product.state = False
            product.save()
            return Response(
                {"message": "Producto eliminado correctamemte."},
                status=status.HTTP_200_OK
            )
        return Response({"error":"No existe un producto con esos datos"},status=status.HTTP_400_BAD_REQUEST)

# Actualizacion de elemento
class ProductUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self, pk): # indica que es lo que se va a regresar
        return self.get_serializer().Meta.model.objects.filter(state=True).filter(id=pk).first()
    
    # Aqui ahora PATCH me va solo a devolver el objeto, ya no lo actualiza
    def patch(self, request, pk=None):
        product = self.get_queryset(pk)
        if product:
            product_serializer = self.serializer_class(product)
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        return Response({"error":"No existe un producto con esos datos"},status=status.HTTP_400_BAD_REQUEST)

    # Personalizar el funcionamiento de PUT
    def put(self, request, pk=None):
        product = self.get_queryset(pk)
        if product:
            product_serializer = self.serializer_class(product, data=request.data)
            if product_serializer.is_valid():
                product_serializer.save()
                return Response(product_serializer.data, status=status.HTTP_200_OK)
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)