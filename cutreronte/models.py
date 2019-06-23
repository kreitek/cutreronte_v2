from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from telegramapp.models import GrupoTelegram
from telegramapp.utils import cutretelegram_enviar_mensaje


class Sitio(models.Model):
    CERRADO = 0
    ABIERTO = 1

    ESTADO = [
        (CERRADO, 'Cerrado'),
        (ABIERTO, 'Abierto'),
    ]

    estado = models.IntegerField(choices=ESTADO, default=CERRADO)

    @staticmethod
    def get_estado():
        sitio_unico, _ = Sitio.objects.get_or_create(id=1)
        return sitio_unico.estado

    @staticmethod
    def get_estado_str():
        estado_actual = Sitio.get_estado()
        for estado, estado_str in Sitio.ESTADO:
            if estado == estado_actual:
                return estado_str
        return None

    @staticmethod
    def abrir():
        sitio_unico, _ = Sitio.objects.get_or_create(id=1)
        sitio_unico.estado = Sitio.ABIERTO
        sitio_unico.save()
        Sitio.notificar_estado("Espacio abierto")

    @staticmethod
    def cerrar():
        sitio_unico, _ = Sitio.objects.get_or_create(id=1)
        sitio_unico.estado = Sitio.CERRADO
        sitio_unico.save()
        Sitio.notificar_estado("Espacio cerrado")

    @staticmethod
    def notificar_estado(mensaje_a_enviar):
        grupos_telegram = GrupoTelegram.objects.filter(notificar_estado=True)
        for grupo in grupos_telegram:
            cutretelegram_enviar_mensaje(mensaje_a_enviar, grupo.id_grupo)
        print(mensaje_a_enviar)


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

    def sacar(self):
        if self.estado == Usuario.DENTRO:
            self.estado = Usuario.FUERA
            self.save()
            self.notificar_cambio("ha salido")

    def meter(self):
        if self.estado == Usuario.FUERA:
            self.estado = Usuario.DENTRO
            self.save()
            self.notificar_cambio("ha entrado")

    def notificar_cambio(self, msg):
        mensaje_a_enviar = "{} ({}) {}".format(self.username, self.usuario_telegram, msg)
        grupos_telegram = GrupoTelegram.objects.filter(notificar_cambios=True)
        for grupo in grupos_telegram:
            cutretelegram_enviar_mensaje(mensaje_a_enviar, grupo.id_grupo)
        print(mensaje_a_enviar)


@receiver(pre_save, sender=Usuario)
def usuario_pre_save(sender, instance, **kwargs):
    if not instance.username:  # fuerza que sea null en vez de una cadena vacia, para comprobar que es unico
        instance.username = None
    if not instance.id_telegram:
        instance.id_telegram = None


@receiver(post_save, sender=Usuario)
def usuario_post_save(sender, instance, **kwargs):
    # comprobar lleno o vacio
    usuarios_dentro = Usuario.objects.filter(estado=Usuario.DENTRO).count()
    if usuarios_dentro > 1:
        return  # los cambios son entre 0 y 1, si hay mas de 1 persona dentro no hace falta commprobar mas
    sitio_estado = Sitio.get_estado()
    if sitio_estado == Sitio.ABIERTO and not usuarios_dentro:  # sitio abierto y sale ultimo usuario
        Sitio.cerrar()
    elif sitio_estado == Sitio.CERRADO and usuarios_dentro:  # sitio cerrado y entra alguien
        Sitio.abrir()


class Equipo(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class Dispositivo(models.Model):
    mac = models.CharField(max_length=50, blank=False, null=False, unique=True)
    dispositivo = models.CharField(max_length=50, blank=True, null=True, unique=False
                                   , help_text="Nombre del dispositivo (modelo de telefono), portatil...")
    fabricante = models.CharField(max_length=300, blank=True, null=True, unique=False, default="")
    usuario = models.ForeignKey(Usuario, blank=True, null=True, on_delete=models.SET_NULL)
    equipo = models.ForeignKey(Equipo, on_delete=models.SET_NULL, null=True, )
    created = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.usuario:
            return "{} ({})".format(self.mac, self.usuario.username)
        else:
            return self.mac


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

