import logging
import os
import random
import time
import vk_api

from google.cloud import dialogflow
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
from tools import detect_intent_texts

logger = logging.getLogger(__name__)


def send_answer(event, vk_api):
    msg = create_msg
    if msg:
        vk_api.messages.send(
            user_id=event.user_id,
            message=msg,
            random_id=random.randint(1,1000)
        )

def create_msg():
    project_id = os.getenv("PROJECT_ID")
    response = detect_intent_texts(project_id, event.user_id, event.text, 'ru')
    if response.query_result.intent.is_fallback:
        return None
    else:
        return response.query_result.fulfillment_text


if __name__ == '__main__':
    load_dotenv()

    logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
 
    google_application_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    vk_token = os.getenv("VK_TOKEN")
    
    vk_session = vk_api.VkApi(token=vk_token)
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
             

