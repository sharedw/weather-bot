import requests  # noqa
from fetch import DataFetcher
from save_data import DataSaver
from Draw import DataDrawer
from time import sleep




print("File opened...")
if __name__ == "__main__":

    print('Main function started...')

    dsaver = DataSaver()
    dfetcher = DataFetcher()
    dDrawer = DataDrawer()

    for i in range(180):
        try:
            curr_data = dfetcher.fetch_all()
            dsaver.insert_data(curr_data)
            dDrawer.draw_weather(curr_data)
        except Exception:
            pass
        sleep(60)