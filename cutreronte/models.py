from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Usuario(models.Model):
    FUERA = 0
    DENTRO = 1

    ESTADO = [
        (FUERA, 'Fuera'),
        (DENTRO, 'Dentro'),
    ]

    username = models.CharField(max_length=50, blank=False, null=False, unique=True)
    autorizado = models.BooleanField(default=False)
    estado = models.IntegerField(choices=ESTADO, default=FUERA)
    usuario_telegram = models.CharField(max_length=50, blank=True, null=True, unique=True, default=None)
    id_telegram = models.IntegerField(blank=True, null=True, unique=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

@receiver(pre_save, sender=Usuario)
def usuario_pre_save(sender, instance, **kwargs):
    if not instance.username:  # fuerza que sea null en vez de una cadena vacia, para comprobar que es unico
        instance.username = None
    if not instance.id_telegram:
        instance.id_telegram = None


class Dispositivo(models.Model):
    mac = models.CharField(max_length=50, blank=False, null=False, unique=True)
    dispositivo = models.CharField(max_length=50, blank=True, null=True, unique=False
                                   , help_text="Nombre del dispositivo (modelo de telefono), portatil...")
    usuario = models.ForeignKey(Usuario, blank=True, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.usuario:
            u = self.usuario.username
        else:
            u = "sin usuario asignado"
        return "{} ({})".format(self.mac, u)


class Rfid(models.Model):
    rfid = models.CharField(max_length=11, blank=False, null=False, unique=True)
    usuario = models.ForeignKey(Usuario, blank=True, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.usuario:
            u = self.usuario.username
        else:
            u = "sin usuario asignado"
        return "{} ({})".format(self.rfid, u)
