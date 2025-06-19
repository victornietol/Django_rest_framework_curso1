from rest_framework.authentication import get_authorization_header
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from apps.users.authentication import ExpiringTokenAuthentication

class Authentication(object):
    user = None # Variables para manejo en la expiracion del token
    user_token_expired = False # Variables para manejo en la expiracion del token

    def get_user(self, request):
        token = get_authorization_header(request).split() # Obtener el valor del header correspondiente
        if token:
            try:
                token = token[1].decode() # Obtener el valor del token
            except:
                return None
            else: # Si todo sale correcto
                token_expire = ExpiringTokenAuthentication()
                user, token, message, self.user_token_expired = token_expire.authenticate_credentials(token)
                
                if user != None and token != None:
                    self.user = user
                    return user
                return message
                
        return None

    def dispatch(self, request, *args, **kwargs):
        user = self.get_user(request)
        # Se encontro un token en la peticion
        if user is not None:
            if type(user) == str:
                response = Response({"error": user, "expired": self.user_token_expired}, status=status.HTTP_400_BAD_REQUEST) # En este caso, por el tipo de clase se debe generear el Response asi
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                return response
            
            if not self.user_token_expired:
                return super().dispatch(request, *args, **kwargs)
        #Si no se encuentra token en la peticion
        response = Response(
            {"error": "No se han enviado credenciales.", "expired": self.user_token_expired},
            status=status.HTTP_400_BAD_REQUEST
        ) # En este caso, por el tipo de clase se debe generear el Response asi
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        return response