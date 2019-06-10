# Django (hay que lanzarlo con manage.py telegram
from django.conf import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from .tasks import COMANDOS_TELEGARM_DISPONIBLES, start, error, mensaje, comandos_telegram
import logging


logger = logging.getLogger(__name__)

# Start the bot.
# Create the EventHandler and pass it your bot's token.
updater = Updater(settings.TELEGRAM_TOKEN)

# Get the dispatcher to register handlers
dp = updater.dispatcher
bot = dp.bot  # para poder mandar mensajes

# on different commands - answer in Telegram
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler(list(COMANDOS_TELEGARM_DISPONIBLES.keys()), comandos_telegram))

# on noncommand i.e message - echo the message on Telegram
dp.add_handler(MessageHandler(Filters.text, mensaje))

# log all errors
dp.add_error_handler(error)

# Start the Bot
updater.start_polling()

# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
# updater.idle() # en common/management/commands/telegram.py
