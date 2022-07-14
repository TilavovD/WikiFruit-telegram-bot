import requests
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

URL = "https://fruityvice.com/api/fruit"
FRUITS_LIST = 'SHOW ALL FRUITS'
ABOUT = 'ABOUT'
HELP = 'HELP'

buttons = [
    [FRUITS_LIST],
    [ABOUT, HELP],
]

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def get_fruit_url(fruit_name):
    """
    Get fruit data from FruityVice
    """
    return requests.get(f"{URL}/{fruit_name}").json()


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_text(
        text=f'Hi {user.first_name}!\n\n'
             f'Welcome to WikiFruit! \n\n'
             f'Type /help or press HELP button for guidance',
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        f'All commands:\n/start - starts bot\n'
        f'/help - shows hints\n'
        f'/find - gives info about fruits\n'
        f'LIST - shows all available fruits')


def about_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('This is WikiFruit bot: the bot which gives information about fruits. \n\n'
                              'To see the names of all available fruits press\n <SHOW ALL FRUITS>\n button')


def find_command(update: Update, context: CallbackContext) -> None:
    """Give info about particular fruit"""
    if update.message.text == "/find":
        list_command(update, context)
    else:
        message_splited = update.message.text.split(' ')
        fruit = " ".join(message_splited[1::])
        response = get_fruit_url(fruit)
        if response is not None:
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
    """Shows the list of all fruits"""
    response = get_fruit_url("all")
    text = 'Available fruits:\n\n'
    for fr in response:
        text += f'{fr["name"]}\n'
    update.message.reply_text(
        f"{text}\n\nNote: Search like this: \ne.g.  /find Apple"
    )


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5555202844:AAHaArQSzqTP_ajkhlJdB1eOAWO0UsiJ-8M")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("find", find_command))
    dispatcher.add_handler(CommandHandler("list", list_command))
    dispatcher.add_handler(MessageHandler(Filters.text(FRUITS_LIST), list_command))
    dispatcher.add_handler(MessageHandler(Filters.text(ABOUT), about_command))
    dispatcher.add_handler(MessageHandler(Filters.text(HELP), help_command))

    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, help_command))

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
