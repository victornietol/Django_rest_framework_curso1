from rest_framework import serializers
from apps.users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Serializadores custom para autenticacion con SimpleJWT
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","username", "email", "name", "last_name")



# Serializador para devolver campos especificos al usar Auth
class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "name", "last_name")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    # Sobreescribir metodo para poder cifrar contraseñas
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"]) # Cifrar password
        user.save()
        return user
    
    # Sobreescribir para cifrar la contraseña
    def update(self, instance, validated_data):
        update_user = super().update(instance, validated_data)
        update_user.set_password(validated_data["password"]) # Cifrar password
        update_user.save()
        return update_user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

    # Asignando manualmente los campos que se regresaran al utilzar el serializador
    # Es lo que se convierte en json y se devuelve en la peticion
    # Aunque arriba en fields indique que quiero todos los campos, con esto solo me muestra los que yo defino
    def to_representation(self, instance):
        # data = super().to_representation(instance) # Este es el que viene por defecto
        data = {
            "id": instance["id"], # El nombre de las keys puedo asignarlas como yo quiera dependiendo de que nombre quiera que se muestre en la respuesta (esto no cambia mi modelo original)
            "username": instance["username"], # Si al usar el serializador pido objects.all() entonces utilizo instance.username, si se usa objects.values(<campos>) entonces se usa con corchetes
            "email": instance["email"],
            "name": instance["name"]
        }
        return data
    

class UserLogoutSerializer(serializers.Serializer):
    pass


# Serializador para Actualizaciones
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "name", "last_name")












# Prueba de validaciones personalizadas y definir metodos personalizados con diferente logica para
# funciones create(), update(), save() de cada serializador definido
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