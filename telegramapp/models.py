from django.db import models


class GrupoTelegram(models.Model):
    nombre = models.CharField(max_length=50)
    id_grupo = models.IntegerField(blank=False, null=False, unique=True)
    permite_expulsar = models.BooleanField(default=False)
    notificar_estado = models.BooleanField(default=False)  # notifica abierto cerrado
    notificar_cambios = models.BooleanField(default=False)  # notifica entra sale de cada usuario

    def __str__(self):
        return self.nombre
