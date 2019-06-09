from django.db import models
from cutreronte.models import Dispositivo

class Prueba(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class RegistroMac(models.Model):
    FUERA = 0
    DENTRO = 1

    ESTADO = [
        (FUERA, 'Fuera'),
        (DENTRO, 'Dentro'),
    ]

    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    estado = models.IntegerField(choices=ESTADO, default=DENTRO)
    tiempo = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.dispositivo.mac
