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
            (W / 2, 140),
            f"{curr_data['text']}",
                **small_font_options
        )

        # Main Temp
        draw.text(
            (400, 100), f"{curr_data['tempf']}°F", font=large_font, fill=0, anchor="mm"
        )

        weather_icon = (
            Image.open("icons/day/partly_cloudy.png")
            .convert("RGBA")
            .resize((75, 75), Image.NEAREST)
        )
        image.paste(weather_icon, (550, 80), weather_icon)

        # Divider
        draw.line([(100, 160), (700, 160)], fill=0, width=2)
        draw.line([(400, 160), (400, 480)], fill=0, width=2)

        # rain stats
        draw.text(
            (200, 240),
            f"Daily Rain: {curr_data['dailyrainin']} in",
            font=small_font,
            fill=0,
            anchor="mm",
        )
        draw.text(
            (200, 265),
            f"Event Rain: {curr_data['eventrainin']} in",
            font=small_font,
            fill=0,
            anchor="mm",
        )
        draw.text(
            (200, 290),
            f"Monthly Rain: {curr_data['monthlyrainin']} in",
            font=small_font,
            fill=0,
            anchor="mm",
        )

        # temp stats
        draw.text(
            (600, 240),
            f"Temp: {curr_data['tempf']}°F",
            **small_font_options
        )
        draw.text(
            (600, 265),
            f"Humidity: {curr_data['humidity']}%",
            **small_font_options
        )
        draw.text(
            (600, 290),
            f"Feels Like: {round(curr_data['feelsLike'], 1)}°F",
            font=small_font,
            fill=0,
            anchor="lm",
        )
        draw.text(
            (600, 315),
            f"Wind Speed/Gust: {round(curr_data['windspeedmph'], 1)}, {round(curr_data['windgustmph'], 1)} mph",
            font=small_font,
            fill=0,
            anchor="mm",
        )
        temp_plot = (
            Image.open("plots/temperature.png")
            .convert("RGBA")
            #resize((800, 800), Image.BICUBIC)
        )
        image.paste(temp_plot, (370, 180), temp_plot)

        self.epd.display(self.epd.getbuffer(image))
        #sleep(3)
        #epd.Clear()
        #epd.sleep()
