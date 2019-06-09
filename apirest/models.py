from django.db import models

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

    mac = models.CharField(max_length=30)
    estado = models.IntegerField(choices=ESTADO, default=DENTRO)
    tiempo = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mac
