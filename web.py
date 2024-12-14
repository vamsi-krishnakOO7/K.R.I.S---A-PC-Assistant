import requests
import webbrowser
from ui import update_ui
from speech import ui_speak
import time


USER_NAME = "ENTER USER NAME"

WEATHER_API_KEY = 'f3a25d117cf5885922dbd5e24d1e04a3'
NEWS_API_KEY = 'fcbb93e0d18049ca81a28e4c5f708cf9'

def perform_web_search(query):
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)
    update_ui(f"Performing web search for: {query}")
    ui_speak(f"Okay {USER_NAME}, Here are the search results.")
    
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    weather_data = response.json()
      # Check if the response contains the 'weather' and 'main' keys
    if 'weather' in weather_data and 'main' in weather_data:
        weather_description = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        weather_report = f"Weather in {city}: {weather_description}, Temperature: {temperature}°C"
        update_ui(weather_report)
        ui_speak(weather_report)
    elif 'message' in weather_data:
        # If there's a message key, it usually contains information about what went wrong (e.g., city not found, invalid API key)
        error_message = weather_data['message']
        update_ui(f"Error fetching weather data: {error_message}")
        ui_speak(f"Error fetching weather data: {error_message}")
    else:
        # General error handling if the response structure is not as expected
        update_ui("Failed to retrieve weather data.")
        ui_speak("Sorry, but I have failed to retrieve the requested weather data.")

def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    news_data = response.json()
    
    intro_str="Here are the top five news headlines from around the world"
    update_ui(intro_str)
    ui_speak(intro_str)
    
    for article in news_data['articles'][:5]:  # Get top 5 headlines
        news_title = article['title']
        update_ui(news_title)
        ui_speak(news_title)
        time.sleep(1)