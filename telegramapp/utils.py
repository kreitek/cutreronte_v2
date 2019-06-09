from django.conf import settings
from django.utils.http import quote
import urllib.request
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
