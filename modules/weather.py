import requests

API_KEY = "d85c1aadf248fabcb0bc754add11e56e"


def get_weather(city):

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    try:
        response = requests.get(url, timeout=6)

    except requests.exceptions.ConnectionError:
        return {
            "Error": (
                "No internet connection. Please check your "
                "network and try again."
            )
        }

    except requests.exceptions.Timeout:
        return {
            "Error": (
                "The weather service took too long to respond. "
                "Please try again."
            )
        }

    except requests.exceptions.RequestException as e:
        return {
            "Error": f"Could not reach the weather service: {e}"
        }

    try:
        data = response.json()
    except ValueError:
        return {
            "Error": "Received an invalid response from the weather service."
        }

    if response.status_code != 200:
        return {
            "Error": data.get("message", "Unknown error")
        }

    try:
        return {
            "City": data["name"],
            "Temperature": f'{data["main"]["temp"]} °C',
            "Humidity": f'{data["main"]["humidity"]}%',
            "Weather": data["weather"][0]["description"].title(),
            "Wind Speed": f'{data["wind"]["speed"]} m/s'
        }
    except (KeyError, IndexError):
        return {
            "Error": "Unexpected response format from the weather service."
        }