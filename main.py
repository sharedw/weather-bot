import requests  # noqa
from DataHandler import DataHandler
from Draw import DataDrawer
from time import sleep




print("File opened...")
if __name__ == "__main__":

    print('Main function started...')

    dhandler = DataHandler()
    dDrawer = DataDrawer()

    for i in range(1):

        curr_data = dhandler.fetch_all(cache=True)

        print(curr_data)
        dDrawer.draw_weather(curr_data)

        sleep(0.1)