import duckdb #noqa
import pandas as pd
import json


class DataSaver():

    def __init__(self):
        self.DB_PATH = "weather.duckdb"
        self.TABLE_NAME = "observations"
        self.con = duckdb.connect(self.DB_PATH)
        self.con.execute(f"""create table if not exists {self.TABLE_NAME} (
            dateutc bigint, 
            tempf double, 
            humidity double, 
            windspeedmph double, 
            windgustmph double, 
            maxdailygust double, 
            winddir double, 
            uv double, 
            solarradiation double, 
            hourlyrainin double, 
            eventrainin double, 
            dailyrainin double, 
            weeklyrainin double,  
            monthlyrainin double,
            totalrainin double, 
            battout double, 
            tempinf double, 
            humidityin double, 
            baromrelin double, 
            baromabsin double, 
            feelsLike double, 
            dewPoint double, 
            feelsLikein double, 
            dewPointin double, 
            lastRain timestamp, 
            tz varchar,
            date timestamp,
            text string,
            icon string,
            code int,
            alert string,
            )
            """)

    def insert_data(self, record):
        df = pd.DataFrame([record])
        self.con.register('new_data', df)
        self.con.execute(f'INSERT INTO {self.TABLE_NAME} SELECT * FROM new_data')
        df = self.con.sql('select * from observations').df()
        print(df)
        return


with open('sample_data.json') as f:
    curr_data = json.load(f)

ds = DataSaver()
ds.insert_data(curr_data)