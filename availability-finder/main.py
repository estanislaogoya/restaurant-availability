import logging
import os
from dotenv import load_dotenv
import requests
import datetime
import json
import settings
import run

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    force=True,
)

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def _send_to_tg(msg):
    TOKEN = os.environ['TOKEN']
    CHAT_ID = os.environ['CHAT_ID']
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}"
    return requests.get(url) # this sends the message


if __name__ == "__main__":
    run.run()