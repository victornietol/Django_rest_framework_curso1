# Serializers que dependen del objeto producto

from rest_framework import serializers

from apps.products.models import Product
from apps.products.api.serializers.general_serializers import MeasureUnitSerializer, CategoryProductSerializer

class ProductSerializer(serializers.ModelSerializer):
    # Esto dos campos (measure_unit, category_product) se definen 
    # asi para al mostrar el valor del campo en lugar
    # de mostrar el numero correspondiente a la FK, por lo tanto, ahora muestra la
    # clase (tabla o entidad de la BD) a la que hace referencia la relacion.

    # FORMA 1 (muestra todos los detalles de la entidad con la que hace realacion):
    # measure_unit = MeasureUnitSerializer()
    # category_product = CategoryProductSerializer()

    # FORMA 2 (muestra el valor str del modelo al que hace referencia la FK, aqui los modelos son
    # MeasureUnit y CategoryProduct):
    # measure_unit = serializers.StringRelatedField()
    # category_product = serializers.StringRelatedField()

    class Meta:
        model = Product
        exclude = ("state","created_date","modified_date","deleted_date")

    # FORMA 3 (con to_representation, es lo que va a devolver completo a la peticion):
    def to_representation(self, instance):
        return {
            "id":instance.id,
            "name": instance.name,
            "description": instance.description,
            #"image": instance.image if instance.image != "" else "",
            "image": instance.image.url if instance.image and hasattr(instance.image, "url") else "",
            "measure_unit": instance.measure_unit.description if instance.measure_unit is not None else "",
            "category_product": instance.category_product.description if instance.category_product is not None else ""
        }