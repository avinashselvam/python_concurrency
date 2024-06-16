from datetime import datetime
import requests
import os

PINCODES = []

API_KEY = os.environ['API_KEY']

def make_response(success, message, data = None):
    return {
        "sucess": success,
        "message": message,
        "data": data
    }

def get_weather(pincode, todays_date = datetime.today().strftime('%Y-%m-%d')):

    endpoint = lambda pincode, date1: f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{pincode}/{date1}?key={API_KEY}"

    try:
        weather_api_response = requests.get(endpoint(pincode, todays_date))
        weather_api_response.raise_for_status()
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        response = make_response(False, http_err), 503
    except Exception as err:
        print(f"Other error occurred: {err}")
        response = make_response(False, err), 503
    else:
        print("Success!")
        response_json = weather_api_response.json()
        response = {'message': 'success', 'weather': response_json}, 200
    return response

def print_temperature(pincode, weather):
    print(f'temp at {pincode} is {weather["weather"]["days"][0]["temp"]}')

def task(pincode):
    weather = get_weather(pincode)
    print_temperature(pincode, weather)
