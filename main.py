from DataHandler import DataHandler
from Draw import DataDrawer
from time import sleep # noqa

print("File opened...")
if __name__ == "__main__":
    print("Main function started...")

    dhandler = DataHandler()
    dDrawer = DataDrawer()

    while True:
        try:
            curr_data = dhandler.fetch_all(cache=False)
            #just save matplotlib plots
            print(curr_data)
            dDrawer.draw_weather(curr_data)
        except Exception as e:
            print(e)
            pass
        sleep(60)
