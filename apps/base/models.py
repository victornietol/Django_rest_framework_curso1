from django.db import models

# Modelo base para otros modelos
class BaseModel(models.Model):
    '''Model definition for BaseModel'''

    # TODO: define fields here
    id = models.AutoField(primary_key=True)
    state = models.BooleanField("Estado", default=True)
    created_date = models.DateField("Fecha de creacion", auto_now=False, auto_now_add=True)
    modified_date = models.DateField("Fecha de modificacion", auto_now=True, auto_now_add=False)
    deleted_date = models.DateField("Fecha de eliminacion", auto_now=True, auto_now_add=False)

    class Meta:
        abstract = True # Indica que va a funcionar como una super clase para los modelos que hereden de este modelo, por lo tanto, no se crea tabla de este modelo en la BD pero si de sus hijas
        verbose_name = "Modelo Base"
        verbose_name_plural = "Modelos Base"