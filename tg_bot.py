import logging
import os

from google.cloud import dialogflow
from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def send_msg(update: Update, context: CallbackContext):
    msg = detect_intent_texts(
    PROJECT_ID, update.message.chat_id, update.message.text, 'ru')
    update.message.reply_text(msg)
    
    
def detect_intent_texts(project_id, session_id, text, language_code):    
  session_client = dialogflow.SessionsClient()
  session = session_client.session_path(project_id, session_id)
  text_input = dialogflow.TextInput(text=text, language_code=language_code)
  query_input = dialogflow.QueryInput(text=text_input)
  response = session_client.detect_intent(session=session, query_input=query_input)
  return response.query_result.fulfillment_text


def main():
    load_dotenv()
    tg_token = os.getenv("TG_TOKEN")
    google_application_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    project_id = os.getenv("PROJECT_ID")

    logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
    
    updater = Updater(TG_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, send_msg))
    dispatcher.add_error_handler(logger.error("Something happend"))
    updater.start_polling()


if __name__ == '__main__':
    main()
