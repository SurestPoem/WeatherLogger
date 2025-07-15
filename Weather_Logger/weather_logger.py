import requests as req
import csv
import os

weather_code_dict = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snowfall",
    73: "Moderate snowfall",
    75: "Heavy snowfall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Slight or moderate thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}

def get_weather_code_description(code):
    return weather_code_dict.get(code, "Unknown weather code")


def get_current_weather(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
	    "latitude": latitude,
	    "longitude": longitude,
	    "current": ["temperature_2m", "apparent_temperature", "relative_humidity_2m", "weather_code", "precipitation", "cloud_cover", "wind_speed_10m", "wind_direction_10m"]
    }

    response = req.get(url, params=params)

    if response.status_code != 200:
        print(f"Status code: {response.status_code}")
        return None
    
    responsejson = response.json()

    date, time = responsejson['current']['time'].split('T')
    date = date.replace('-', '/')

    weather_data = {
        'log_datetime': responsejson['current']['time'],
        'log_date': date,
        'log_time': time,
        'temperature': responsejson['current']['temperature_2m'],
        'feels_like': responsejson['current']['apparent_temperature'],
        'humidity': responsejson['current']['relative_humidity_2m'],
        'weather_code': get_weather_code_description(responsejson['current']['weather_code']),
        'precipitation': responsejson['current']['precipitation'],
        'cloud_cover': responsejson['current']['cloud_cover'],
        'wind_speed': responsejson['current']['wind_speed_10m'],
        'wind_direction': responsejson['current']['wind_direction_10m']
    }

    return weather_data


def save_weather_data_to_csv(weather_data, filename='WeatherLogger/Weather_Logger/weather_log.csv'):
    fieldnames = weather_data.keys()
    existing_timestamps = set()

    if os.path.exists(filename):
        with open(filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            existing_timestamps = {row['log_datetime'] for row in reader}
    else:
        existing_timestamps = set()

    if weather_data['log_datetime'] in existing_timestamps:
        print("Entry for this datetime already exists. Skipping write.")
        return

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(weather_data)
        print("Weather data saved successfully.")

weather_data = get_current_weather(54.3268, -2.7476)
if weather_data:
    save_weather_data_to_csv(weather_data)