from time import sleep
import requests  # noqa
from PIL import Image, ImageDraw, ImageFont
import yaml


import platform

if platform.system() == "Windows":
    import mock_epd as epd7in5_V2

    title_font_path = "C:/Windows/Fonts/arialbd.ttf"
    large_font_path = "C:/Windows/Fonts/arialbd.ttf"
    small_font_path = "C:/Windows/Fonts/arial.ttf"
else:
    from waveshare_epd import epd7in5_V2

    title_font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    large_font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    small_font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


# Setup your API key and location
API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"
CITY = "Copperas Cove,US"
UNITS = "imperial"  # or 'metric'

DEVICE_URL = "https://api.ambientweather.net/v1/devices"

DB_PATH = "weather.duckdb"
TABLE_NAME = "ambient_weather"


def fetch_weather_data() -> dict:
    """Fetch weather data from Ambient Weather API."""
    url = "https://api.ambientweather.net/v1/devices"
    params = yaml.safe_load(open("secrets.yaml"))
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        for device in data:
            print(device["lastData"])  # weather data
    else:
        print("Error:", response.status_code, response.text)
    return data[0]["lastData"]


def get_current_conditions(station_id="KGRK"):
    """Fetch current weather conditions from the National Weather Service."""
    headers = {"User-Agent": "(weather-dashboard, sharedwestover@gmail.com)"}
    obs = requests.get(
        f"https://api.weather.gov/stations/{station_id}/observations/latest",
        headers=headers,
    )

    return obs.json()["properties"]['textDescription']


def draw_weather(curr_data):
    epd = epd7in5_V2.EPD()
    epd.init()
    epd.Clear()
    W, H = (800, 480)
    image = Image.new("1", (W, H), 255)  # 800 is width, 480 is height. 0,0 at top left
    draw = ImageDraw.Draw(image)

    # Fonts
    title_font = ImageFont.truetype(title_font_path, 32)
    large_font = ImageFont.truetype(large_font_path, 72)
    small_font = ImageFont.truetype(small_font_path, 24)

    # Title
    draw.text((400, 20), f"Weather - {CITY}", font=title_font, fill=0, anchor="mm")

    # Main Temp
    draw.text(
        (400, 120), f"{curr_data['tempf']}°F", font=large_font, fill=0, anchor="mm"
    )

    # Divider
    draw.line([(100, 190), (700, 190)], fill=0, width=2)

    # Other Stats
    draw.text(
        (200, 240),
        f"Rain: {curr_data['dailyrainin']} in",
        font=small_font,
        fill=0,
        anchor="mm",
    )
    draw.text(
        (600, 240),
        f"Humidity: {curr_data['humidity']}%",
        font=small_font,
        fill=0,
        anchor="mm",
    )
    
    draw.text(
        (W/2, 60),
        f"{curr_data['textDescription']}",
        font=small_font,
        fill=0,
        anchor="mm",
    )
    epd.display(epd.getbuffer(image))
    sleep(3)
    epd.Clear()
    epd.sleep()


print("File opened...")
if __name__ == "__main__":
    print("Main function started...")
    curr_data = fetch_weather_data()
    curr_data['textDescription'] = get_current_conditions()
    print("got weather")
    draw_weather(curr_data)
    print("drawn weather")
