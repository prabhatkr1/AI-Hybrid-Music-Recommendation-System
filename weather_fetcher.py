import requests
import os

def get_weather(city):
    api_key = os.getenv("API_KEY")

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    res = requests.get(url)
    
    # Agar API fail ho jaye
    if res.status_code != 200:
        return "Unknown", 0

    data = res.json()

    # Safe check
    if "weather" not in data or "main" not in data:
        return "Unknown", 0

    weather = data["weather"][0]["main"]
    temp = data["main"]["temp"]

    return weather, temp
