import logging
import os
import random
import time
import vk_api

from google.cloud import dialogflow
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType


logger = logging.getLogger(__name__)


def send_anwer(event, vk_api):
    msg = detect_intent_texts(PROJECT_ID, event.user_id, event.text, 'ru')
    if msg:
        vk_api.messages.send(
            user_id=event.user_id,
            message=msg,
            random_id=random.randint(1,1000)
        )
    
def detect_intent_texts(project_id, session_id, text, language_code):    
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    if response.query_result.intent.is_fallback:
        return None
    else:
        return response.query_result.fulfillment_text


if __name__ == '__main__':
    load_dotenv()

    logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    PROJECT_ID = os.getenv("PROJECT_ID")
    VK_TOKEN = os.getenv("VK_TOKEN")
    
    vk_session = vk_api.VkApi(token=VK_TOKEN)
    longpoll = VkLongPoll(vk_session)
    vk_api = vk_session.get_api()
    timer = 3
    
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    send_answer(event, vk_api)
        except Exception as error:
            logging.exception(error)
            time.sleep(timer)
             

