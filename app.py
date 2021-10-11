from flask import Flask
from flask import request
from flask import redirect
from urllib.request import urlopen
from flask import render_template
from flask.helpers import url_for
from weather_client import WeatherClient
import json


app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip = request.environ['REMOTE_ADDR']
    else:
        ip = request.environ['HTTP_X_FORWARDED_FOR']

    url = f'http://ipinfo.io/{ip}/json'
    response = urlopen(url)
    data = json.load(response)
    city = data['city']
    client = WeatherClient()
    weather_prognosis = client.weather_prognosis(city)
    day_info = weather_prognosis['day_info']
    prognosis = weather_prognosis['week_info']
            
    return render_template('main.html', succes = True, temperature = day_info['temp'], city = city, prognosis = prognosis)
        

@app.route('/search', methods = ['GET'])
def city_search():

    try:
        city = request.args.get('city')
        client = WeatherClient()
        weather_prognosis = client.weather_prognosis(city)
        day_info = weather_prognosis['day_info']
        prognosis = weather_prognosis['week_info']
                
        return render_template('main.html', succes = True, temperature = day_info['temp'], city = city, prognosis = prognosis)
    except:
        return render_template('main.html', succes = False)


if __name__ == '__main__':
    app.run(debug=True)
