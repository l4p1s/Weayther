import requests
import pprint
import json


def predict_wether(lat , lon, date_):
    api_key = 'c2be9bc0a17d49498ecbccee5e86810a'
    hours = 24

    url = f'https://api.weatherbit.io/v2.0/forecast/hourly?lat={lat}&lon={lon}&hours={hours}&key={api_key}'

    response = requests.get(url)
    data = json.loads(response.text)
    for i_ in data["data"]:
        if(i_["datetime"] == date_):
            print(f"Time: {date_}")
            print(f"locate lat : {lat}     lon  : {lon}")
            print(f"Temperature: {i_['temp']}°C")
            print(f"Wind Speed: {i_['wind_spd']} m/s")
            print(f"Weather: {i_['weather']['description']}")
            print("-" * 20)

if __name__ == '__main__':
    print("これは天気予報を取得するapiを用いたコードです")