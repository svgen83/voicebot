import logging
import os

from google.cloud import dialogflow
from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


load_dotenv()
TG_TOKEN = os.getenv("TG_TOKEN")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
PROJECT_ID = os.getenv("PROJECT_ID")


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext):
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext):
    msg = detect_intent_texts(PROJECT_ID, update.message.chat_id, update.message.text, 'ru')
    update.message.reply_text(msg)
    
    
def detect_intent_texts(project_id, session_id, text, language_code):    
  session_client = dialogflow.SessionsClient()
  session = session_client.session_path(project_id, session_id)
  text_input = dialogflow.TextInput(text=text, language_code=language_code)
  query_input = dialogflow.QueryInput(text=text_input)
  response = session_client.detect_intent(session=session, query_input=query_input)
  return response.query_result.fulfillment_text



def main():
    updater = Updater(TG_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
