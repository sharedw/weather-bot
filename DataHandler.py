import duckdb  # noqa
import pandas as pd
import json
import requests  # noqa
import yaml
import matplotlib.pyplot as plt


class DataHandler:
    def __init__(self):
        self.DB_PATH = "weather.duckdb"
        self.TABLE_NAME = "observations"
        self.DEVICE_URL = "https://api.ambientweather.net/v1/devices"
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
        self.con.register("new_data", df)
        self.con.execute(f"INSERT INTO {self.TABLE_NAME} SELECT * FROM new_data")
        df = self.con.sql("select * from observations").df()
        print(df)
        return

    def query(self, query_text):
        return self.con.query(query_text)

    def query_latest_data(self):
        record = self.query("select * from observations order by dateutc desc limit 1")
        return record

    def fetch_weather_data(self) -> dict:
        """Fetch weather data from Ambient Weather API."""
        url = "https://api.ambientweather.net/v1/devices"
        params = yaml.safe_load(open("secrets.yaml"))
        params = {k: params[k] for k in ("applicationKey", "apiKey")}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            curr_data = response.json()[0]["lastData"]
        else:
            print("Error:", response.status_code, response.text)

        return curr_data

    def fetch_weatherapi_data(self):
        params = yaml.safe_load(open("secrets.yaml"))
        weatherapi_key = params["weatherapi"]
        condition_url = f"http://api.weatherapi.com/v1/current.json?key={weatherapi_key}&q=31.1708409,-97.8459396&aqi=no"
        alert_url = f"http://api.weatherapi.com/v1/alerts.json?key={weatherapi_key}&q=31.1708409,-97.8459396"

        conditions = requests.get(condition_url)
        if conditions.status_code == 200:
            conditions = conditions.json()["current"]["condition"]

        alerts = requests.get(alert_url)
        if alerts.status_code == 200:
            alerts = alerts.json()["alerts"]["alert"]
            if len(alerts) > 0:
                conditions["alert"] = alerts[0]["headline"]
            else:
                conditions["alert"] = ""

        return conditions
    
    def plot_temp(self):
        var = 'tempf'
        df = self.con.sql(f"""select date AT TIME ZONE 'UTC' AT TIME ZONE 'America/Chicago' AS cst_time,
                    {var} from observations 
                    where date >= CURRENT_DATE - INTERVAL 3 DAY""").df()

        df['mov'] = df[var].rolling(1).mean()
        dpi = 129
        figsize = (3.5, 2)

        fig, ax = plt.subplots(figsize=figsize, dpi=dpi)


        fig.patch.set_alpha(0.0)       # Transparent figure background
        ax.set_facecolor('none')       # Transparent plot background

        unique_days = df['cst_time'].dt.normalize().drop_duplicates()
        plt.xticks(unique_days, unique_days.dt.strftime('%a'), rotation=0, fontsize=12, fontweight='bold')
        plt.xlim(unique_days.min(), unique_days.max())
        plt.yticks(rotation=0, fontsize=14, fontweight='bold')
        ax.set_ylabel('Temp', fontsize=14, fontweight='bold', fontname='DejaVu Sans Mono')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.plot(df['cst_time'], df['mov'], color='black', linewidth=3)
        #ax.plot(df['cst_time'], df[var])


        plt.tight_layout()
        plt.savefig("plots/temperature.png", dpi=129, bbox_inches='tight')
        return 

    def plot_rain(self):
        var = 'monthlyrainin'
        df = self.con.sql(f"""
            SELECT date AT TIME ZONE 'UTC' AT TIME ZONE 'America/Chicago' AS cst_time,
                {var}
            FROM observations
            WHERE EXTRACT(MONTH FROM date AT TIME ZONE 'America/Chicago') = EXTRACT(MONTH FROM CURRENT_DATE)
            AND EXTRACT(YEAR FROM date AT TIME ZONE 'America/Chicago') = EXTRACT(YEAR FROM CURRENT_DATE)
        """).df()

        df['mov'] = df[var].rolling(1).mean()
        dpi = 129
        figsize = (3.5, 2)

        fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

        fig.patch.set_alpha(0.0)
        ax.set_facecolor('none')

        _, ymax = ax.get_ylim()
        if ymax < 2:
            ax.set_ylim(0, 2)

        unique_days = df['cst_time'].dt.normalize().drop_duplicates()
        plt.xticks(unique_days, unique_days.dt.strftime('%a'), rotation=0, fontsize=12, fontweight='bold')
        plt.xlim(unique_days.min(), unique_days.max())
        plt.yticks(rotation=0, fontsize=14, fontweight='bold')
        ax.set_ylabel('Temp', fontsize=14, fontweight='bold', fontname='DejaVu Sans Mono')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.plot(df['cst_time'], df['mov'], color='black', linewidth=3)
        plt.tight_layout()
        plt.savefig("plots/rain.png", dpi=129, bbox_inches='tight')
        print("PLOT GOT SAVEDF")
        return 

    def fetch_all(self, cache=False):
        if not cache:
            curr_data = self.fetch_weather_data()
            curr_data.update(self.fetch_weatherapi_data())
            self.insert_data(curr_data)

        else:
            curr_data = self.query_latest_data().df().to_dict(orient="records")[0]
        
        self.plot_temp()
        self.plot_rain()
        return curr_data


def test_save():
    with open("sample_data.json") as f:
        curr_data = json.load(f)

    ds = DataHandler()
    ds.insert_data(curr_data)
    return


# test_save()

# ds = DataSaver()
# record = ds.query_latest_data()
