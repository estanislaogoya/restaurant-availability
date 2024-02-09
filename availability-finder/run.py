import settings
import requests
import datetime
import logging
import json
import os
import processing

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def _generate_url(restaurant_id, search_type, num_people):
 return f"https://api.meitre.com/api/calendar-availability-new/{restaurant_id}/{num_people}/{search_type}"


def run():
    exito = False
    errors = []
    try:
        while exito == False:

            for restaurant_name, restaurant_key in settings.restaurants.items():

                results = []

                logger.info(f"\U0001F916 Processing Restaurant: {restaurant_name}")

                for search_type in settings.reservation_type:

                    rsp = requests.get(_generate_url(restaurant_key, search_type, settings.num_people), headers=settings.headers)
                    logger.debug(f"Response content: {rsp.text}")

                    if not rsp.content:
                        logger.warning(f"Empty response for restaurant: {restaurant_name}")
                        continue

                    if rsp.status_code != 200:
                        logger.info(f"Response error: {rsp.text}")
                    else:
                        try:
                            rsp_json = rsp.json()
                            #logger.info(f"Response error: {rsp_json}")
                            processed_result = processing._process_result(rsp_json, restaurant_key, search_type, settings.num_people)
                            if len(processed_result) > 0:
                                results.append(processed_result)
                        except json.JSONDecodeError as e:
                            logger.error(f"Error decoding JSON response for restaurant {restaurant_name}: {e}")
                            continue  # Skip processing this planta if there's a JSON decoding error
                
                if len(results) == 0:
                    logger.info(f"\u274C No results found for this restaurant")
            settings._sleep()

    except Exception as e:
        errors.append(e)
        logger.error(f"Exception happened: {e}")
        # if os.environ['SEND_TO_BOT'].lower() == 'true': 
        #     pass
            #_send_to_tg(f"Exception happened: {e}")
    return errors