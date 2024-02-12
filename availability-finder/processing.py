import datetime
import logging
import os
import settings
import requests

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


# Function to check if a date is within threshold
def is_within_hourly_threshold(hour_string):
    # Concatenate the placeholder date and the time text
    datetime_text = f"1900-01-01 {hour_string}"

    # Parse the string to datetime object
    datetime_object = datetime.datetime.strptime(datetime_text, '%Y-%m-%d %H:%M')

    hour = datetime_object.hour

    #logger.info(f"Available Hour: {hour}; Max Hour: {settings.search_criteria['dinner']['hour_min']}")

    if (
        settings.search_criteria['lunch']['hour_min'] <= hour <= settings.search_criteria['lunch']['hour_max']
        ) or (
        settings.search_criteria['dinner']['hour_min'] <= hour <= settings.search_criteria['dinner']['hour_max']):
        return True
    return False

def _process_result(json_str, restaurant_key, type, num_people):

    results = []
    try:
        if "calendarInfo" in json_str:
            # Iterate through each element in calendarInfo
            for item in json_str["calendarInfo"]:
                    date_str = item.get('date')
                    is_available = item.get('isAvailable', 0)  # Default value is 0 if 'isAvailable' key is missing

                    if date_str and is_available == 1:
                        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')
                        # Check if the date is earlier than the maximum date
                        if settings.search_criteria['date_min'] <= date_obj <= settings.search_criteria['date_max']:
                            # Check if the hour portion of the date is within the threshold
                            hourly_results = _process_hours(date_obj.date(), restaurant_key, type, num_people)
                            if len(hourly_results) > 0:
                                results.append(hourly_results)
                        else:
                            pass
                            #print(f"Date {date_str} is not earlier than max date: {settings.search_criteria['date_max']}")
        else:
            print("JSON data is not available.")

    except Exception as e:
        logger.error(f"Exception happened: {e}")
    
    return results

def _process_hours(date_str, key, type, num_people):

    results = []
    
    generate_url = f"https://api.meitre.com/api/search-all-hours/en/{num_people}/{date_str}/{type}/{key}"
    rsp = requests.get(generate_url, headers=settings.headers)

    if not rsp.content:
        logger.warning(f"Empty response for restaurant id: {key}")
        return

    if rsp.status_code != 200:
        logger.info(f"Response error: {rsp.text}")
    else:
        rsp_json = rsp.json()
        if 'center' in rsp_json:
            rsp_obj = rsp_json['center']
            # logger.info(f"Response content: {rsp_json['center']}")
            for slot in rsp_obj['slots']:
                if slot['type'] != 'No':
                     
                     if is_within_hourly_threshold(slot['hour']):
                        menus = []
                        if 'menus' in slot:
                            for menu in slot['menus']:
                                if menu['disabled'] is False:
                                    menus.append(menu['name'])
                        
                        logger.info(f"\u2705 Availability on {date_str} for {num_people} people of type {slot['type']} at : {slot['hour']}. Menus: {menus}")
                        results.append(f"Availability on {date_str} for {num_people} people of type {slot['type']} at : {slot['hour']}. Menus: {menus}")

    return results

    # if is_within_threshold(date_str):
    #     print("Date {} is within threshold and earlier than max date.".format(date_str))
    # else:
    #     print("Date {} is earlier than max date, but hour is not within threshold.".format(date_str))

