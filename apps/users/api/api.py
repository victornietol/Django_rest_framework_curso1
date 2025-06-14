from rest_framework import status
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.users.models import User
from apps.users.api.serializers import UserSerializer, TestUserSerializer

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
        users_serializer = UserSerializer(users, many=True)
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

