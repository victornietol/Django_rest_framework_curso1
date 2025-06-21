from rest_framework import status
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from apps.users.models import User
from apps.users.api.serializers import UserSerializer, TestUserSerializer, UserListSerializer, UpdateUserSerializer


#### UTILIZANDO CLASES PARA USERS ####
class UserViewSet(viewsets.GenericViewSet):
    model = User # Es lo mismo que acceder a 'self.serializer_class.Meta.model'
    serializer_class = UserSerializer
    list_serializer_class = UserListSerializer
    queryset = None

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.filter(is_active=True).values("id","username","email","name")
        return self.queryset

    def list(self, request):
        users = self.get_queryset()
        users_serializer = self.list_serializer_class(users, many=True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                "message": "Usuario creado correctamente.",
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "Hay errores en el registro",
            "errors": user_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Detalles de un solo usuario
    def retrieve(self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = self.serializer_class(user)
        return Response(user_serializer.data)
    
    def update(self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = UpdateUserSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                "message": "Usuario actualizado correctamente."
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "Hay errores al actualizar."
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        user_destroy = self.model.objects.filter(id=pk).update(is_active=False) # Regresa el numero de registros modificados
        if user_destroy == 1:
            return Response({
                "message": "Usuario eliminado correctamente."
            })
        return Response({
            "message": "No existe el usuario que desea eliminar"
        }, status=status.HTTP_404_NOT_FOUND)







class UserAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        users_serializer = UserSerializer(users, many=True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)



# Utilizando un decorador
# Hace lo mismo que la clase anterior para manejar las peticiones, pero aqui se hace con una funcion
@api_view(['GET', 'POST'])
def user_api_view(request):
    
    if request.method == "GET": # Si es peticion GET entonces hace lo mismo que la clase de arriba
        '''
        # Probando metodo de validacion personalizado
        test_data = {
            "name": "palabra",
            "email": "prohibida@cvp.com"
        }
        test_user = TestUserSerializer(data=test_data, context=test_data) # Si se le pasa el context entonces se puede obtener la info enviada para validar desde metodos especificos
        if test_user.is_valid():
            print("Paso validaciones")
        else:
            print(test_user.errors)
        '''

        users = User.objects.all().values("id","username","email","password")
        users_serializer = UserListSerializer(users, many=True) # Se utiliza otro serializador para cambiar los se muestra en la peticion
        return Response(users_serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "POST": #Crear usuario
        user_serializer = UserSerializer(data=request.data) # Convertir al modelo
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST) # Si falla



# Obtener detalles de un objeto,  actualizar un objeto, eliminar un objeto
@api_view(["GET", "PUT", "DELETE"])
def user_detail_api_view(request, pk=None):
    user = User.objects.filter(id=pk).first()
    if user:
        if request.method == "GET":
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data)

        elif request.method == "PUT":
            user_serializer = UserSerializer(instance=user, data=request.data) # (Instancia del usuario a modificar, informacion nueva del usuario)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_200_OK)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == "DELETE":
            user.delete()
            return Response({"message:""Usuario eliminado."}, status=status.HTTP_200_OK)
    
    return Response(
        {"message":"No se ha encontrado el usuario"}, 
        status=status.HTTP_400_BAD_REQUEST
    )

