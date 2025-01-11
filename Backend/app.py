from flask import Flask
from flask import request
from flask import Response
from datetime import datetime
from zoneinfo import ZoneInfo
from timezonefinder import TimezoneFinder

import json
import requests

app = Flask(__name__)

def getForecastFromLatLon(lat, lon):
    lat = float(request.args.get('lat'))
    lon= float(request.args.get('lon'))
    tz = TimezoneFinder()
    timezone = tz.timezone_at(lat=lat, lng=lon)
    gridForecastData = requests.get(f"https://api.weather.gov/points/{lat},{lon}")
    forecastLink = gridForecastData.json()["properties"]["forecastHourly"]
    forecastResponse = requests.get(forecastLink)
    forecastData = forecastResponse.json()["properties"]["periods"]
    filtered_forecast_data = [{"startTime": datetime.fromisoformat(item["startTime"]).astimezone(ZoneInfo(timezone)).strftime("%Y-%m-%d %H:%M:%S %Z").split(" ")[:2], "endTime": datetime.fromisoformat(item["endTime"]).astimezone(ZoneInfo(timezone)).strftime("%Y-%m-%d %H:%M:%S %Z").split(" ")[:2], "temperature": item["temperature"], "relativeHumidity": item["relativeHumidity"]["value"], "windVector": [item["windSpeed"][:-4], item["windDirection"]]} for item in forecastData]   

    return filtered_forecast_data


@app.route('/getFullForecastFromLatLon', methods=['GET'])
def getFullForecastFromLatLon():
    lat = float(request.args.get('lat'))
    lon= float(request.args.get('lon'))
    return Response(
        json.dumps(getForecastFromLatLon(lat, lon)).encode('utf-8')
    )


@app.route('/getCurrentForecastFromLatLon', methods=['GET'])
def getCurrentForecastFromLatLon():
    lat = float(request.args.get('lat'))
    lon= float(request.args.get('lon'))
    return Response(
        json.dumps(getForecastFromLatLon(lat, lon)[0]).encode('utf-8')
    )

@app.route('/getFWI', methods=['GET'])
def getFWI():
    lat = float(request.args.get('lat'))
    lon= float(request.args.get('lon'))
    forecastData = getForecastFromLatLon(lat, lon)[0]
    temperature = float(forecastData["temperature"])
    humidity = float(forecastData["relativeHumidity"])
    wind_speed = float(forecastData["windVector"][0])
    print(temperature, humidity, wind_speed)
    ffmc = (temperature - 10) * (100 - humidity) / 100 
    isi = wind_speed * (temperature / 10)  
    fwi = ffmc * isi / 100
    return Response(
        json.dumps(fwi).encode('utf-8')
    )
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
