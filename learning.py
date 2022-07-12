import argparse
import json
import logging
import os
import sys

from google.cloud import dialogflow
from dotenv import load_dotenv


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)
    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)
    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )
    response = intents_client.create_intent(request={"parent": parent, "intent": intent})
    logging.info("Интент добавлен")


if __name__ == '__main__':

    load_dotenv()
    
    logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
    )

    google_application_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    project_id = os.getenv("PROJECT_ID")
    
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="введите путь к файлу с фразами")
    args = parser.parse_args()
    
    with open(args.path, "r") as questions:
      phrases = json.load(questions)
      
    
    for phrase in phrases.items():
        display_name, dialog_elements = phrase
        questions = dialog_elements["questions"]
        answer = dialog_elements["answer"]
        create_intent(project_id, display_name, questions, [answer])

