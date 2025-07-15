import platform
from PIL import Image, ImageDraw, ImageFont
from time import sleep

if platform.system() == "Windows":
    import mock_epd as epd7in5_V2

    title_font_path = "C:/Windows/Fonts/arialbd.ttf"
    large_font_path = "C:/Windows/Fonts/arialbd.ttf"
    small_font_path = "C:/Windows/Fonts/arial.ttf"
else:
    from waveshare_epd import epd7in5_V2 #noqa

    title_font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    large_font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    small_font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

CITY = "Copperas Cove,US"


class DataDrawer():
    
    def draw_weather(self,curr_data):
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
            f"Daily Rain: {curr_data['dailyrainin']} in",
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
            f"{curr_data['text']}",
            font=small_font,
            fill=0,
            anchor="mm",
        )

        if curr_data['alert'] != "":
            draw.text(
                (W/2, 60),
                f"{curr_data['alert']}",
                font=ImageFont.truetype(small_font_path, 16),
                fill=0,
                anchor="mm",
            )
        epd.display(epd.getbuffer(image))
        sleep(3)
        epd.Clear()
        epd.sleep()