from time import sleep
import requests #noqa
from PIL import Image, ImageDraw, ImageFont
import yaml
from waveshare_epd import epd7in5_V2  # Adjust to your version (e.g., epd7in5b_V2 for black/red)

# Setup your API key and location
API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"
CITY = "Copperas Cove,US"
UNITS = "imperial"  # or 'metric'

DEVICE_URL = 'https://api.ambientweather.net/v1/devices'

DB_PATH = 'weather.duckdb'
TABLE_NAME = 'ambient_weather'

def fetch_weather_data() -> dict:
	"""Fetch weather data from Ambient Weather API."""
	url = 'https://api.ambientweather.net/v1/devices'
	params = yaml.safe_load(open('secrets.yaml'))
	response = requests.get(url, params=params)
	if response.status_code == 200:
		data = response.json()
		for device in data:
			print(device['lastData'])  # weather data
	else:
		print('Error:', response.status_code, response.text)
	return data[0]['lastData']


def draw_weather(curr_data):
    epd = epd7in5_V2.EPD()
    epd.init()
    epd.Clear()

    image = Image.new('1', (epd.height, epd.width), 255)  # landscape
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)

    draw.text((10, 10), f"Weather in {CITY}", font=font, fill=0)
    draw.text((10, 50), f"Temp: {curr_data['tempf']}°", font=font, fill=0)
    draw.text((10, 90), f"Event rain: {curr_data['dailyrainin']}", font=font, fill=0)
    draw.text((10, 130), f"Humidity: {curr_data['humidity']}%", font=font, fill=0)
    image = image.rotate(0, expand=True)
    epd.display(epd.getbuffer(image))
    sleep(3)
    epd.Clear()
    epd.sleep()

print("File opened...")
if __name__ == "__main__":
    print('Main function started...')
    curr_data = fetch_weather_data()
    print("got weather")
    draw_weather(curr_data)
    print("drawn weather")