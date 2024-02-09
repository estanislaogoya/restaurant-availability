from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv
import logging
import time

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

restaurants = {
    'La Ferneteria Serrano' : '735',
    'La Ferneteria Bellas Artes' : '882',
    'Anchoita' : '154',
    'Don Julio' : '25',
    'La Cabrera Palermo' : '60',
    'El Preferido' : '186'
}

today_date = datetime.today().date()
future_date = today_date + timedelta(days=5)

# Define default values
default_max_date = future_date.strftime('%Y-%m-%d')
default_min_date = today_date.strftime('%Y-%m-%d')
default_dinner_hour_max = 24
default_dinner_hour_min = 20
default_lunch_hour_max = 15
default_lunch_hour_min = 12

num_people = int(os.environ['NUM_PEOPLE'])

search_criteria = {
    'date_max' : datetime.strptime(os.getenv('MAX_DATE', str(default_max_date)), '%Y-%m-%d' ).replace(tzinfo=timezone(timedelta(hours=-3))),
    'date_min' : datetime.strptime(os.getenv('MIN_DATE', str(default_min_date)), '%Y-%m-%d' ).replace(tzinfo=timezone(timedelta(hours=-3))),
    'dinner': {
        'hour_max' : int(os.getenv('DINNER_HOUR_MAX', default_dinner_hour_max)),
        'hour_min' : int(os.getenv('DINNER_HOUR_MIN', default_dinner_hour_min)),
    },
    'lunch': {
        'hour_max' : int(os.getenv('LUNCH_HOUR_MAX', default_lunch_hour_max)),
        'hour_min' : int(os.getenv('LUNCH_HOUR_MIN', default_lunch_hour_min)),
    }
}


headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Host": "api.meitre.com",
    "Origin": "https://elpreferido.meitre.com",
    "Referer": "https://elpreferido.meitre.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}

reservation_type = [
    'dinner',
    'lunch'
]

def _sleep():
    logger.info(f"sleeping: {int(os.environ['SLEEP_TIME_IN_SEC'])} seconds")
    time.sleep(int(os.environ['SLEEP_TIME_IN_SEC']))