# VISTA DE LOGIN

from datetime import datetime

# Para eliminar sesiones activas
from django.contrib.sessions.models import Session

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

##### Autenticacion custom modificando y utilizando SimpleJWT ########
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.api.serializers import (
    CustomTokenObtainPairSerializer, CustomUserSerializer
)
from apps.users.models import User

class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(
            username = username,
            password = password
        ) # Verifica que exista un usuario con esas credenciales
        if user:
            login_serializer = self. serializer_class(data=request.data)
            if login_serializer.is_valid():
                user_serializer = CustomUserSerializer(user)
                return Response({
                    "token": login_serializer.validated_data.get("access"),
                    "refresh-token": login_serializer.validated_data.get("refresh"),
                    "user": user_serializer.data,
                    "message": "Custom: Inicio de sesion exitoso."
                }, status=status.HTTP_200_OK)
            return Response({"error":"Contraseña o nombre de usuario incorrectos."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error":"Contraseña o nombre de usuario incorrectos."}, status=status.HTTP_400_BAD_REQUEST)








####### Vistas personalizadas para la autenticacion con tokens #################

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from apps.users.authentication_mixins import Authentication
from apps.users.api.serializers import UserTokenSerializer, UserLogoutSerializer

# Vista para renovar token
class UserToken(Authentication, APIView):
    '''
    Validate token
    '''
    def get(self, request, *args, **kwargs):
        #username = request.GET.get("username")
        # Verificar que el usuario tenga un token
        try:
            user_token, _ = Token.objects.get_or_create(user = self.user)
            user = UserTokenSerializer(self.user)
            return Response({
                "token": user_token.key,
                "user": user.data
            }, status=status.HTTP_200_OK)
        except:
            return Response(
                {"error": "Credenciales enviadas incorrectas."},
                status=status.HTTP_400_BAD_REQUEST
            )

class LoginCustom(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # Este serializador ya contiene los campos username y password
        login_serializer = self.serializer_class(data=request.data, context={"request":request})
        # Verifica existencia del usuario enviado (username, password)
        if login_serializer.is_valid():
            # Si existe el usuario
            user = login_serializer.validated_data['user'] # Acceder al usuario recibido (en este caso username y password)
            # Validar que el usuario este activo
            if user.is_active:
                # Si esta activo Crear o validar token
                token, created = Token.objects.get_or_create(user=user)
                user_serializer = UserTokenSerializer(user) # Serializador especial creado para mostrar ciertos campos
                if created:
                    # Si el token se acaba de crear (inicio de sesion)
                    return Response(
                        {
                            "token": token.key,
                            "user": user_serializer.data,
                            "message": "Inicio de sesion exitoso."
                        },
                        status=status.HTTP_201_CREATED
                    )
                else:
                    # Si se quiere iniciar sesion cuando ya hay una sesion activa

                    
                    # Si se quieren cerrar todas las sesion activas y solo dejar la actual 
                    # o ultima (esto quiere decir que solo se puede iniciar sesion en un lugar a 
                    # la vez)
                    all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
                    if all_sessions.exists():
                        for session in all_sessions:
                            session_data = session.get_decoded()
                            if user.id == int(session_data.get('_auth_user_id')):
                                session.delete()

                    token.delete()
                    token = Token.objects.create(user=user)
                    return Response(
                        {
                            "token": token.key,
                            "user": user_serializer.data,
                            "message": "Inicio de sesion exitoso."
                        },
                        status=status.HTTP_201_CREATED
                    )

                    # Si solo se quiere permitir iniciar sesion si no hay una sesion activa
                    #token.delete()
                    #return Response({"error":"Ya se ha iniciado sesion con este usuario"}, status=status.HTTP_409_CONFLICT)
            else:
                return Response({"error":"El usuario no puede iniciar sesion"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"error":"Username o password incorrectos."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error en el usuario"}, status=status.HTTP_400_BAD_REQUEST)
    

# El logout se puede hacer por GET o POST
class LogoutCustom(APIView):
    def get(self, request, *args, **kwargs):
        try:
            token = request.GET.get("token")
            token = Token.objects.filter(key=token).first()
            if token:
                user = token.user

                all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
                if all_sessions.exists(): # Cerrar sesion si existe sesion
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()
                token.delete()

                session_message = "Sesiones de usuario eliminadas."
                token_message = "Token eliminado."
                return Response(
                    {"token_message": token_message, "session_message": session_message},
                    status=status.HTTP_200_OK
                )
            return Response({"error":"No se ha encontrado un usuario con estas credenciales"},
                            status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error":"No se ha encontrado token en la peticion"},
                            status=status.HTTP_409_CONFLICT)
    
        

class Logout(GenericAPIView):
    serializer_class = UserLogoutSerializer # Serializador vacio para que no muestre error
    def post(self, request, *args, **kwargs):
        user = User.objects.filter(id=request.data.get("user", 0))
        if user.exists():
            RefreshToken.for_user(user.first())
            return Response({"message": "Sesion cerrada correctamente."}, status=status.HTTP_200_OK)
        return Response({"error":"El usuario no existe."}, status=status.HTTP_400_BAD_REQUEST)