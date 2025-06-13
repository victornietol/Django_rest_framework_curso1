from rest_framework import serializers
from apps.users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

# Prueba de validaciones personalizadas
class TestUserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length = 200)
    email = serializers.EmailField()

    # Las funcione para validar se ejecutan en el orden: validate_<campos>() -> validate()
    # validate() se ejecuta hasta el final
    def validate_name(self, value): ## Debe llevar el nombre de cada campo a validar
        if "palabra_prohibida" in value:
            raise serializers.ValidationError("Error, palabra prohibida")
        return value
    
    def validate_email(self, value):
        # Acceder al contexto del elemento (se puede acceder a la informacion completa enviada)
        # Con esto se accede al valor de otro campo
        if self.validate_name(self.context["name"]) in value: # Campo name
            raise serializers.ValidationError("El email no puede contener el nombre")

        if value == "":
            raise serializers.ValidationError("Se debe indicar un correo")
        return value
    
    def validate(self, data):
        # Esta validacion se puede hacer en el campo especifico pero accediendo con context como 
        # se muestra en validate_email, por lo tanto, el error lo indicara en ese campo 
        #if data["name"] in data["email"]:
        #    raise serializers.ValidationError("El email no puede contener el nombre")
        return data