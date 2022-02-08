import logging
import os
import vars
from pathlib import Path

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

from model.Linien import Linien
from model.Search import Search
from model.Tafel import Tafel
from util import make_fahrplan, make_selection_text

from parser import parse, unparse

path = Path(os.path.dirname(os.path.realpath(__file__)))

# logging config
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: %(message)s')

file_handler = logging.FileHandler(path / 'log/bot.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(vars.welcomeMessage)


def mainHandler(update: Update, _: CallbackContext) -> None:
    """Echo the user message."""
    search = Search(update.message.text)
    update.message.reply_text(vars.selectHaltestelleText, reply_markup=search.reply_markup())
    logger.info(f'text: {update.message.text}\nfrom: {update.message.from_user}')


def button_answer(update: Update, _: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    # print(query.data)
    cmd, *rest = query.data.split()
    args = parse(rest)

    if cmd == 'haltestelle':
        query.answer('Linie auswählen')
        linienObj = Linien(args.haltestelle)  # linien der Haltestelle laden
        query.edit_message_text(
            text=vars.selectLinieText,
            reply_markup=linienObj.reply_markup(unparse('t', args.haltestelle)),
        )
    elif cmd == 'add':
        oldCmd = query.message.reply_markup.to_dict()['inline_keyboard'][-1][-1]['callback_data']
        query.answer('Linie auswählen')
        linienObj = Linien(args.haltestelle)  # linien der Haltestelle laden
        fahrplan_cmd, selectedLinien = make_fahrplan(oldCmd, args.linieToAdd)
        if oldCmd != fahrplan_cmd:  # nachricht hat sich verändert
            query.edit_message_text(
                text=make_selection_text(selectedLinien),
                reply_markup=linienObj.reply_markup(fahrplan_cmd),
                parse_mode='HTML'
            )
    elif cmd == 't':  # tafel
        tafel = Tafel(args.haltestelle, args.linien, args.richtung, args.verkehrsmittel)
        reply_markup = tafel.reply_markup()
        if query.message.text != str(tafel) or query.message.reply_markup != reply_markup:
            query.answer('updating')
            query.edit_message_text(
                text=tafel.telegram_str(),
                reply_markup=reply_markup,
                parse_mode='HTML'
            )
        else:
            query.answer('Daten sind aktuell')
    else:
        query.answer()
    logger.info(f'callback: {query.data}\nfrom: {query.from_user}')


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(vars.token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text, mainHandler))

    dispatcher.add_handler(CallbackQueryHandler(button_answer))

    # Start the Bot
    logger.info("polling now")
    print("polling now")
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
