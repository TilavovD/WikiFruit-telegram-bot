import requests
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

URL = "https://fruityvice.com/api/fruit"

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
def get_fruit_url(fruit_name):
    """
    Get fruit data from FruityVice
    """

    return requests.get(f"{URL}/{fruit_name}").json()


# Define a few command handlers. These usually take the two arguments update and
# context.


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_text(
        f'Hi {user.full_name}!\n'
        f'Welcome to WikiFruit! Here you can find any information about any fruit.'
        f'Type /help for guidance'
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        f'All commands:\n/start - starts bot\n'
        f'/help - shows hints\n'
        f'/find - gives info about fruits\n'
        f'/list - shows all available fruits')


def find_command(update: Update, context: CallbackContext) -> None:
    """Give info about particular fruit"""

    fruit = "all"
    if update.message.text != "/find":
        message_splited = update.message.text.split(' ')
        fruit = " ".join(message_splited[1::])

    response = get_fruit_url(fruit)
    if fruit == 'all':
        text = 'Available fruits:\n\n'
        for fr in response:
            text += f'{fr["name"]}\n'

        update.message.reply_text(
            f"{text}\n\nNote: Search like this: \ne.g.  /find Apple"
        )

    elif response is not None:
        update.message.reply_text(
            f'{response["name"]}:\n\nFamily: {response["family"].capitalize()}\n'
            f'Genus: {response["genus"].capitalize()}\n'
            f'Nutritions:\n'
            f' - carbohydrates: {response["nutritions"]["carbohydrates"]}\n'
            f' - protein: {response["nutritions"]["protein"]}\n'
            f' - fat: {response["nutritions"]["fat"]}\n'
            f' - calories: {response["nutritions"]["calories"]}\n'
            f' - sugar: {response["nutritions"]["sugar"]}')

    else:
        update.message.reply_text(
            'fruit not found.')


def list_command(update: Update, context: CallbackContext) -> None:
    if update.message.text == "/list":
        response = get_fruit_url('all')
        text = 'Available fruits:\n\n'
        for fr in response:
            text += f'{fr["name"]}\n'
        update.message.reply_text(
            f"{text}\n\nNote: Search like this: \ne.g.  /find Apple"
        )
    else:
        update.message.reply_text(
            'Type /list to view full list')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("find", find_command))
    dispatcher.add_handler(CommandHandler("list", list_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
