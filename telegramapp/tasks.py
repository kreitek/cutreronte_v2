from django.urls import reverse
from django.utils.http import quote
from django.conf import settings
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup # https://python-telegram-bot.readthedocs.io/en/stable/
import urllib.request
import json
import re
import logging


logger = logging.getLogger(__name__)

def cutretelegram_enviar_mensaje(msg, chatid):
    if not chatid or not msg:
        return
    api_telegram = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
    url = api_telegram.format(settings.TELEGRAM_TOKEN, chatid, quote(msg))
    # logging.info(url)
    try:
        urllib.request.urlopen(url, timeout=2)
        logging.debug("Enviado por telegram: '{}'".format(msg))
    except Exception as e:
        logging.error(e)


def reverse_no_i18n(viewname, *args, **kwargs):
    # https://stackoverflow.com/questions/27680748/when-using-i18n-patterns-how-to-reverse-url-without-language-code
    result = reverse(viewname, *args, **kwargs)
    m = re.match(r'(/[^/]*)(/.*$)', result)
    return m.groups()[1]


def start(bot, update):
    """ No comprueba registro """
    update.message.reply_text('Bienvenido! .')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.error('Update "{}" caused error "{}"'.format(update, error))

def mensaje(bot, update):
    """ mensaje estandar (no es comando)."""
    update.message.reply_text(update.message.text)

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
    'ayuda':  "Muestra esta ayuda",
}
# NOTA: para actualizar los comandos en el bot: python manage.py comandos_telegram
# list(COMANDOS_TELEGARM_DISPONIBLES.keys())
