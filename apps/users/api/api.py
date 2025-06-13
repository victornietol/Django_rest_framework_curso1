from rest_framework import status
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.users.models import User
from apps.users.api.serializers import UserSerializer

class UserAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        users_serializer = UserSerializer(users, many=True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)

# Utilizando un decorador
# Hace lo mismo que la clase anterior para manejar las peticiones, pero aqui se hace con una funcion
@api_view(['GET', 'PUT'])
def user_api_view(request):
    if request.method == "GET": # Si es peticion GET entonces hace lo mismo que la clase de arriba
        users = User.objects.all()
        users_serializer = UserSerializer(users, many=True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "PUT":
        user_serializer = UserSerializer(data=request.data) # Convertir al modelo
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST) # Si falla