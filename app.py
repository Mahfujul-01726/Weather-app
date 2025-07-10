from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# OpenWeatherMap API details
API_KEY = "4a71aa79c305c72e2151c768aea8542e"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city):
    """Fetches weather data for a given city."""
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        # Log the full error response for better debugging
        if e.response:
            print(f"Error fetching weather data: {e.response.status_code} - {e.response.text}")
        else:
            print(f"Error fetching weather data: {e}")
        return None


def process_weather_data(data):
    """Processes raw weather data into a structured format."""
    if not data or data.get('cod') != 200:
        return "not_found"
    return {
        'city': data['name'],
        'temperature': round(data['main']['temp']),
        'humidity': data['main']['humidity'],
        'description': data['weather'][0]['description'].title(),
    }


@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    if request.method == 'POST':
        city = request.form['city']
        weather_data = get_weather(city)
        weather = process_weather_data(weather_data)
    return render_template('index.html', weather=weather)


if __name__ == "__main__":
    app.run(debug=True)
