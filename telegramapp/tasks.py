from django.urls import reverse
from django.conf import settings
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup # https://python-telegram-bot.readthedocs.io/en/stable/
import json
import re
import logging

from cutreronte.models import Usuario, Sitio

logger = logging.getLogger(__name__)


def reverse_no_i18n(viewname, *args, **kwargs):
    # https://stackoverflow.com/questions/27680748/when-using-i18n-patterns-how-to-reverse-url-without-language-code
    result = reverse(viewname, *args, **kwargs)
    m = re.match(r'(/[^/]*)(/.*$)', result)
    return m.groups()[1]

def comandos_telegram(bot, update):
    """ Todos los comandos llegan aqui (menos start), verifica que este autentificado y lanza comando correspondiente """
    # saltamos la autentificacion
    # user = get_usuario(update)
    # if not user:
    #     usuario_no_registrado(update)
    #     return
    user = None
    # comando_offset = int(update.message.entities[0].offset)
    # no tiene offset, si el comando no va al principio, no salta el callback
    commando_length = int(update.message.entities[0].length)
    comando = update.message.text[1:commando_length]
    COMANDOS_TELEGARM_DISPONIBLES[comando][0](update, user)


def start(bot, update):
    """ No comprueba registro """
    update.message.reply_text('Bienvenido! .')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.error('Update "{}" caused error "{}"'.format(update, error))

def mensaje(bot, update):
    """ mensaje estandar (no es comando)."""
    update.message.reply_text(update.message.text)

def prueba(update, user):
    update.message.reply_text("texto de prueba")

def status(update, user):
    update.message.reply_text("Hangar 3 {}".format(Sitio.get_estado_str()))

def users_in(update, user):
    gente_dentro = Usuario.objects.filter(estado=Usuario.DENTRO)
    if not gente_dentro:
        update.message.reply_text("Nadie dentro")
    else:
        gente_dentro_comas = ",".join(str(usuario.username) for usuario in gente_dentro)
        update.message.reply_text("Estan dentro: {}".format(gente_dentro_comas))

def ayuda(update, user):
    """Send a message when the command /help is issued."""
    respuesta = ""
    for key in COMANDOS_TELEGARM_DISPONIBLES.keys():
        if COMANDOS_TELEGARM_DISPONIBLES[key][1]:
            respuesta += "/{}\t{}\n".format(key, COMANDOS_TELEGARM_DISPONIBLES[key][1])
    print(respuesta)
    update.message.reply_text(respuesta[:-1])

# comando como key, y tupla con funcion y descripcion. Si no tiene descripcion, no se lista en ayuda
COMANDOS_TELEGARM_DISPONIBLES = {
    'status': (status, "Estado del espacio (abierto o cerrado)"),
    'users_in': (users_in, "Usuarios actualmente en el espacio"),
    'prueba': (prueba, None),
    'help': (ayuda, None),
    'ayuda': (ayuda, "Muestra esta ayuda"),
}
# NOTA: para actualizar los comandos en el bot: python manage.py comandos_telegram
# list(COMANDOS_TELEGARM_DISPONIBLES.keys())
