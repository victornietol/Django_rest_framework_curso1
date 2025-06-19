from datetime import timedelta

from django.utils import timezone
from django.conf import settings

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


# Expiracion de token
class ExpiringTokenAuthentication(TokenAuthentication):
    expired = False # Indicar el estado de un token

    def expires_in(self, token):
        time_elapsed = timezone.now() - token.created
        left_time = timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
        return left_time

    def is_token_expired(self, token):
        return self.expires_in(token) < timedelta(seconds=0)

    def token_expire_handler(self, token):
        is_expire = self.is_token_expired(token)
        if is_expire:
            # Cuando el token ha expirado
            self.expired = True
            user = token.user
            token.delete() # Borrar token
            token = self.get_model().objects.create(user=user) # Crear nuevo token (refrescar token), en otros casos se puede hacer otra accion en lugar de esta si se prefiere
        return is_expire, token

    def authenticate_credentials(self, key):
        message, token, user = None, None, None # Para no repetir el mensaje "TOKEN EXPIRADO"
        try:
            token = self.get_model().objects.select_related("user").get(key=key)
            user = token.user
        except self.get_model().DoesNotExist:
            message = "Token invalido"
            self.expired = True
        else:
            # Si se encontro token
            if not token.user.is_active:
                message = "Usuario no activo o eliminado."
            
            is_expired = self.token_expire_handler(token)
            if is_expired:
                message = "Su Token ha expirado."
        
        return (user, token, message, self.expired)