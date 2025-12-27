"""
Flask web application to fetch and display weather 
data based on user-provided latitude and longitude.
"""

from flask import Flask, render_template, request
import requests
from config import API_KEY, BASE_URL

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Handle the main route for the weather application.
    """
    weather_data = None
    if not API_KEY or API_KEY == "your_actual_api_key":
        return {"error": "Error: Please set your OpenWeatherMap API key in config.py"}

    if request.method == "POST":
        lattitude = request.form["latitude"]
        longitude = request.form["longitude"]

        params = {
            "lat": lattitude,
            "lon": longitude,
            "appid": API_KEY,
            "units": "metric",  # Use 'imperial' for Fahrenheit
        }
        response = requests.get(BASE_URL, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # data = json.dumps(d)
            weather_data = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"],
            }
        else:
            # Handle the case where the city is not found
            weather_data = {"error": "City not found"}

    return render_template("index.html", weather=weather_data)


if __name__ == "__main__":
    app.run(debug=True)
