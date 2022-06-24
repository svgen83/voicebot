# Voicebot_bot
This program is designed to answer typical user questions. 

### How to install

Python3 should already be installed.
Then use `pip` (or `pip3` if there is a conflict with Python2) to install the dependencies:
```
pip install -r requirements.txt
```
#### Program setups

In order for the program to work correctly, create an .env file in the program folder containing the following data:

1) Token received upon registration of the telegram bot. You will receive a token upon registration of the bot. It says here [how to register a telegram bot](https://way23.ru/%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F-%D0%B1%D0%BE%D1%82%D0%B0-%D0%B2-telegram/).
Write as follows:
```
TG_TOKEN="Тelegram bot token"
```
2) Project identifier (project ID) [DialogFlow](https://dialogflow.cloud.google.com)
To learn how to create a project, read [here](https://cloud.google.com/dialogflow/es/docs/quick/setup)
Write the project ID like this:
```
PROJECT_ID="created project ID"
```
3) In order for the code to work, you need to download a special json key.
How to do this is described [here](https://cloud.google.com/docs/authentication/getting-started).
Attention! You can download the key only once. But if you accidentally lost it, you can create a new one.
Place the downloaded key on your computer. Better in the folder with the program. And in the .env file, write the path to the key:
```
GOOGLE_APPLICATION_CREDENTIALS="путь к ключу"
```
4) To make the bot work on the Vkontakte social network, create a group in it, and then get a token to interact with the API.
How to get a token is written on [this page](https://dev.vk.com/api/access-token/getting-started). You must give permission to send messages.
```
VK_TOKEN="Vkontakte social network token"
```

#### How to run

The bot is launched from the command line. To run the program using the cd command, you first need to go to the folder with the program.
You should first teach the bot standard phrases. For this you need:
1) download [file with necessary phrases](https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json)
2) run script:
```
python learning.py /path to the file with training phrases
```

To start the telegram bot on the command line, write:
```
python tg_bot.py
```
To launch a chat bot on Vkontakte, respectively::
```
python vk_bot.py
```

To run the program from the server, you must first acquire a server. The following is an example of running on a virtual server [Heroku](https://heroku.com).
The first step is to register on the Heroku website and create an app. You can submit the code from GitHub. After linking your GitHub account to Heroku, you should find the repository with the code and connect it to Heroku. Environment variables should be registered in the Config Vars section in the Settings tab. Click the "Deploy Branch" button.

### Project goal

Code written for educational purposes in an online course for web developers [dvmn.org](https://dvmn.org/).
