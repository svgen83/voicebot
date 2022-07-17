import logging
import os

from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters, CallbackContext
from dialogflow_tools import detect_intent_texts


logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr"Hi {user.mention_markdown_v2()}\!",
        reply_markup=ForceReply(selective=True),
    )


def send_msg(update: Update, context: CallbackContext):
    project_id = os.getenv("PROJECT_ID")
    response = detect_intent_texts(
                                   project_id, update.message.chat_id,
                                   update.message.text, "ru")
    msg = response.query_result.fulfillment_text
    update.message.reply_text(msg)


def error_handler(update, context):
    logger.error("Something happend", exc_info=context.error)
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=context.error)


def main():
    load_dotenv()
    tg_token = os.getenv("TG_TOKEN")
    google_application_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=logging.INFO)

    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command,
                                          send_msg))
    dispatcher.add_error_handler(error_handler)
    updater.start_polling()


if __name__ == "__main__":
    main()

