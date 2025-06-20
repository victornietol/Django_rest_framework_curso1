from rest_framework.authentication import get_authorization_header
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from apps.users.authentication import ExpiringTokenAuthentication

class Authentication(object):
    user = None # Variables para manejo en la expiracion del token

    def get_user(self, request):
        token = get_authorization_header(request).split() # Obtener el valor del header correspondiente
        if token:
            try:
                token = token[1].decode() # Obtener el valor del token
            except:
                return None
            # Si todo sale correcto
            token_expire = ExpiringTokenAuthentication()
            user = token_expire.authenticate_credentials(token)
            
            if user != None:
                self.user = user
                return user
                
        return None

    def dispatch(self, request, *args, **kwargs):
        user = self.get_user(request)
        # Se encontro un token en la peticion
        if user is not None:
            return super().dispatch(request, *args, **kwargs)
        
        #Si no se encuentra token en la peticion
        response = Response(
            {"error": "No se han enviado credenciales."}, status=status.HTTP_400_BAD_REQUEST
        ) # En este caso, por el tipo de clase se debe generear el Response asi
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        return response