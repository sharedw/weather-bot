from DataHandler import DataHandler
from Draw import DataDrawer
from time import sleep # noqa

print("File opened...")
if __name__ == "__main__":
	print("Main function started...")

	dhandler = DataHandler()
	print('handler created')
	dDrawer = DataDrawer()
	print('drawer created')
	try:
		while True:
			curr_data = dhandler.fetch_all(cache=False)
			#just save matplotlib plots
			print(curr_data)
			dDrawer.draw_weather(curr_data)
			sleep(60)

	except KeyboardInterrupt:
		dDrawer.epd.Clear()
		dDrawer.epd.epdconfig.module_exit(cleanup=True)
		sleep(1)