from flask import Flask
from flask import request
from flask import Response
from flask import jsonify
from datetime import datetime
from zoneinfo import ZoneInfo
from timezonefinder import TimezoneFinder
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image, ImageOps
import numpy as np 
import sys
from tensorflow.keras.models import load_model

import json
import requests

app = Flask(__name__)
model = load_model('wildfire_detection_model.h5')




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


@app.route('/detect-fire', methods=['POST'])
def detect_fire():
    # Check if a file is in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    # Get the file from the request
    file = request.files['file']
    result = {}

    # Open the image
    img = Image.open(file)
    img = ImageOps.pad(img, size=(128, 128), color=(0, 0, 0))  # Resize and pad the image
    img_array = img_to_array(img)
    img_array = img_array / 255.0  # Normalize pixel values
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

    # Load the model and make a prediction
    prediction = model.predict(img_array)
    confidence = float(prediction[0][0])

    # Generate response based on the prediction
    if confidence < 0.5:
        result = {'message': 'Fire detected', 'confidence': (1 - confidence) * 100}
    else:
        result = {'message': 'No fire detected', 'confidence': confidence * 100}

    return Response(
        json.dumps(result).encode('utf-8')
    )

 

# @app.route('/detect-fire', methods=['GET'])
# def detect_fire():
#     # if 'file' not in request.files:
#     #     return jsonify({'error': 'No file provided'}), 400
    
#     model = load_model('wildfire_detection_model.h5')
    
# # file = request.files['file']  # Get the uploaded image
#     # img = Image.open(file)
#     image_path = "./grassyhills.jpeg"
#     img = Image.open(image_path)
#     img = ImageOps.pad(img, size=(128, 128), color=(0, 0, 0))  
#     img_array = img_to_array(img)
#     img_array = img_array / 255.0 # normalize pixel
#     img_array = np.expand_dims(img_array, axis=0)

#     prediction = model.predict(img_array)
#     confidence = prediction[0][0]
#     print("Prediction:", prediction)

#     if confidence < 0.5:
#         print(f"Fire detected with {(1 -confidence) * 100:.2f}% confidence.")
#     else:
#         print(f"No fire detected with {confidence * 100:.2f}% confidence.")
    
    
#     return "Checked"



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
