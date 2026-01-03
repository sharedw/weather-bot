# mock_epd.py
from PIL import Image

class EPD:
	width = 800
	height = 480

	def init(self):
		print("EPD initialized (mock)")

	def Clear(self):
		print("EPD cleared (mock)")

	def sleep(self):
		print("EPD sleep (mock)")

	def getbuffer(self, image: Image.Image):
		return image  # just return the PIL image

	def display(self, image):
		image.show()  # or image.save("test_output.png")
		
	def init_part(self):
		return
		
	def display_Partial(self, *args):
		return