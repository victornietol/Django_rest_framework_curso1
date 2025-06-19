# VISTA DE LOGIN

from datetime import datetime

# Para eliminar sesiones activas
from django.contrib.sessions.models import Session

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from apps.users.api.serializers import UserTokenSerializer

class Login(ObtainAuthToken):
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

                    '''
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
                    '''

                    # Si solo se quiere permitir iniciar sesion si no hay una sesion activa
                    token.delete()
                    return Response({"error":"Ya se ha iniciado sesion con este usuario"}, status=status.HTTP_409_CONFLICT)
            else:
                return Response({"error":"El usuario no puede iniciar sesion"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"error":"Username o password incorrectos."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error en el usuario"}, status=status.HTTP_400_BAD_REQUEST)
    

# El logout se puede hacer por GET o POST
class Logout(APIView):
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
    
        