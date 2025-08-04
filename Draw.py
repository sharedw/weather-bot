import platform
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timezone
import pytz

if platform.system() == "Windows":
    print('Windows')
    import mock_epd as epd7in5_V2

    title_font_path = "C:/Windows/Fonts/segoeui.ttf"
    large_font_path = "C:/Windows/Fonts/segoeui.ttf"
    small_font_path = "C:/Windows/Fonts/tahoma.ttf"
else:
    print('LINUX')
    from waveshare_epd import epd7in5_V2  # noqa

    title_font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    large_font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    small_font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

CITY = "Larry's Backyard (Copperas Cove)"


def bigint_to_time(bigint):
    dt_utc = datetime.fromtimestamp(bigint / 1000, tz=timezone.utc)
    cst = pytz.timezone("America/Chicago")
    dt_cst = dt_utc.astimezone(cst)
    cst_str = dt_cst.strftime("%H:%M:%S")
    return cst_str


class DataDrawer:

    def __init__(self):
        self.epd = epd7in5_V2.EPD()
        self.epd.init()
        self.epd.Clear()
        self.counter = 0

    def draw_weather(self, curr_data, graph_data=None):
        W, H = (800, 480)
        image = Image.new(
            "1", (W, H), 255
        )  # 800 is width, 480 is height. 0,0 at top left
        draw = ImageDraw.Draw(image)

        # Fonts
        title_font = ImageFont.truetype(title_font_path, 32)
        large_font = ImageFont.truetype(large_font_path, 72)
        small_font = ImageFont.truetype(small_font_path, 24)
        small_font_options = {
            'font':ImageFont.truetype(small_font_path, 20),
            "anchor":"lm",
        }

        # Title
        draw.text((400, 20), f"{CITY}", font=title_font, fill=0, anchor="mm")
        #update time
        draw.multiline_text(
            (10, 12),
            f"""updated at:\n {bigint_to_time(curr_data["dateutc"])}""",
            font=ImageFont.truetype(small_font_path, 12),
            fill=0,
        )

        # alerts
        print(curr_data)
        if curr_data["alert"] != "":
            draw.text(
                (W / 2, 60),
                f"{curr_data['alert']}",
                **small_font_options
            )

        # description
        draw.text(
            (W / 2, 144),
            f"{curr_data['text']}",
                **small_font_options
        )

        # Main Temp
        draw.text(
            (400, 100), f"{curr_data['tempf']}°F", font=large_font, fill=0, anchor="mm"
        )

        weather_icon = (
            Image.open("icons/day/rainy.png")
            .convert("RGBA")
            .resize((75, 75), Image.NEAREST)
        )
        image.paste(weather_icon, (550, 50), weather_icon)

        # Divider
        draw.line([(100, 160), (700, 160)], fill=0, width=2)
        draw.line([(400, 160), (400, 480)], fill=0, width=2)

        # rain stats
        draw.text(
            (10, 180),
            f"Daily: {curr_data['dailyrainin']:.2f}, Event: {curr_data['eventrainin']:.2f} Month: {curr_data['monthlyrainin']:.2f}",
            **small_font_options 
        )

        rain_plot = (
            Image.open("plots/rain.png")
            .convert("RGBA")
        )
        image.paste(rain_plot, (-30, 240), rain_plot)

        # temp stats
        draw.text(
            (410, 180),
            f"Temp: {curr_data['tempf']}°F, Humidity: {curr_data['humidity']}%",
            **small_font_options
        )
        draw.text(
            (410, 210),
            f"Feels Like: {round(curr_data['feelsLike'], 1)}°F, Wind Speed: {round(curr_data['windspeedmph'], 1)}",
            **small_font_options
        )
        temp_plot = (
            Image.open("plots/temperature.png")
            .convert("RGBA")
        )
        image.paste(temp_plot, (370, 240), temp_plot)

        self.counter = (self.counter + 1) % 11  # cycles 0–10
        if self.counter == 0:
            self.epd.display(self.epd.getbuffer(image))
        else:
            self.epd.display(self.epd.getbuffer(image))
        #sleep(3)
        #epd.Clear()
        #epd.sleep()
