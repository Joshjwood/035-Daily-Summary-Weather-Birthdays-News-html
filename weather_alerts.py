import requests
from privates import *

OWM_Endpoint = OWM_Endpoint
api = api
weather_params = weather_params

def get_weather_data():
    weather_response = requests.get(url=OWM_Endpoint, params=weather_params)
    weather_response.raise_for_status()
    return weather_response.json()

#Temp checker#######
def kelvin_to_c(kelvin):
    return round(kelvin - 273.15, 1)

def tomorrow_weather(weather_data):
    today_day_temp = round(kelvin_to_c(weather_data["daily"][0]["temp"]["day"]), 1)
    tomorrow_day_temp = round(kelvin_to_c(weather_data["daily"][1]["temp"]["day"]), 1)
    day_weather = weather_data["daily"][1]["weather"][0]["description"]

    if today_day_temp > tomorrow_day_temp:
        #tomorrow is colder
        temp_difference = f"{tomorrow_day_temp}c\n That's {round(today_day_temp - tomorrow_day_temp, 1)}c cooler"
    elif today_day_temp < tomorrow_day_temp:
        temp_difference = f"{tomorrow_day_temp}c\n That's {round(tomorrow_day_temp - today_day_temp, 1)}c warmer"
    else:
        temp_difference = f"{tomorrow_day_temp}c - The same as today"

    #tomorrow_forecast =
    return f"<strong>Tomorrow:</strong> {temp_difference} - Expect {day_weather}."

#this is the first chunk of the email because I couldn't get both the title and the 'today' content out seperately and seperate functions arent necessary at this point
def today_weather(weather_data):
    today_day_temp = round(kelvin_to_c(weather_data["daily"][0]["temp"]["day"]), 1)
    tomorrow_day_temp = round(kelvin_to_c(weather_data["daily"][1]["temp"]["day"]), 1)
    day_weather = weather_data["daily"][1]["weather"][0]["description"]

    umbrella_required = 0
    rain_count = 0

    for i in range(0, 12):
        if weather_data["hourly"][i]["weather"][0]["id"] < 700:
            umbrella_required = 1
            rain_count += 1
        else:
            pass

    start_time = 0
    if umbrella_required and weather_data["hourly"][0]["weather"][0]["id"] > 700:
        #if it's going to rain, but it isn't yet
        for i in range(0, 12):
            if weather_data["hourly"][i]["weather"][0]["id"] < 700:
                start_time = int(i)
                break
            else:
                pass
    weather_break = 0
    if umbrella_required and weather_data["hourly"][0]["weather"][0]["id"] < 700:
        #It's currently raining, how long until it gives up
        for i in range(0, 12):
            if weather_data["hourly"][i]["weather"][0]["id"] > 700:
                weather_break = int(i)
                break
            else:
                pass



    if rain_count > 9:
        email_title = "It's going to rain all day"
        email_content = "It's pretty much going to rain all day, the umbrella lives in the car"
    elif rain_count > 1 and rain_count <= 9:
        if weather_data["hourly"][0]["weather"][0]["id"] < 700:
            #it's currently raining
            email_title = "It's raining, but not all day"
            email_content = f"So it's currently raining, but it's not going to rain for the entire day. We're due a reprieve in {weather_break} hours"
        else:
            email_title = "A little rain ahead"
            email_content = f"It's going to rain later, but not all day. Its due to start in {start_time} hours."
    else:
        email_title = "Clear skies ahead"
        email_content = "No rain forecast today"

    return f"{email_title} in Bournemouth.<br><br><strong>Today</strong>:\n{email_content} and it's {today_day_temp} degrees celsius.<br>"

