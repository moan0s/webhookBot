from flask import Flask, Response, request
import simplematrixbotlib as botlib
from config import Config
import logging
import argparse
import asyncio

parser = argparse.ArgumentParser(description='Start the webhook bot.')
parser.add_argument('--config', default=None, help='Specify a configuration file to use')
args = parser.parse_args()

bot_prefix = ""

def setup_bot():
    config = Config(args.config)

    bot_server = config['bot']['server']
    bot_username = config['bot']['username']
    try:
        bot_access_token = config['bot']['access_token']
        creds = botlib.Creds(bot_server,
                             username=bot_username,
                             access_token=bot_access_token)
    except KeyError:
        logging.info("Using password based authentication for the bot")
        try:
            bot_access_password = config['bot']['password']
        except KeyError:
            error = "No access token or password for the bot provided"
            logging.error(error)
            raise KeyError(error)
        creds = botlib.Creds(bot_server,
                             username=bot_username,
                             password=bot_access_password)

    bot_prefix = config['bot']['prefix']


    # Load a config file that configures bot behaviour
    smbl_config = botlib.Config()
    SIMPLE_MATRIX_BOT_CONFIG_FILE = "config.toml"
    try:
        smbl_config.load_toml(SIMPLE_MATRIX_BOT_CONFIG_FILE)
        logging.info(f"Loaded the simple-matrix-bot config file {SIMPLE_MATRIX_BOT_CONFIG_FILE}")
    except FileNotFoundError:
        logging.info(f"No simple-matrix-bot config file found. Creating {SIMPLE_MATRIX_BOT_CONFIG_FILE}")
        smbl_config.save_toml(SIMPLE_MATRIX_BOT_CONFIG_FILE)

    bot = botlib.Bot(creds, smbl_config)
    return bot

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
async def webhook():  # put application's code here
    # Bot sends a message
    print("Dada")
    message = "Dada"
    await bot.api.send_markdown_message("!vnQFpABIvLlxVNtkgM:hyteck.de", message)
    await Response(status=200)

bot = setup_bot()

help_string = "help"

@bot.listener.on_message_event
async def token_actions(room, message):
    match = botlib.MessageMatch(room, message, bot, bot_prefix)
    # Unrestricted commands
    if match.is_not_from_this_bot() and match.contains("help") and match.prefix():
        print(room.room_id)
        """The help command should be accessible even to users that are not allowed"""
        logging.info(f"{match.event.sender} viewed the help")
        await bot.api.send_markdown_message(room.room_id, help_string)

async def main():
    flask_task = asyncio.create_task(app.run())
    bot_task = asyncio.create_task(bot.main())
    await asyncio.gather(flask_task, bot_task)

if __name__ == '__main__':
    asyncio.run(main())





