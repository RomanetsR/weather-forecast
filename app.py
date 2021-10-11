from flask import Flask
from flask import request
from flask import redirect
from urllib.request import urlopen
from flask import render_template
from flask.helpers import url_for
from weather_fuction import Weather_client
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
    weather = Weather_client(city)
    day_info = weather.weather_actual()
    prognosis = weather.weather_prognosis()
            
    return render_template('main.html', temperature = day_info['temp'], city = city, prognosis = prognosis)
        

@app.route('/<city>', methods = ['GET'])
def city_search(city):

    try:
        city = city.capitalize()
        weather = Weather_client(city)
        day_info = weather.weather_actual()
        prognosis = weather.weather_prognosis()
                
        return render_template('main.html', temperature = day_info['temp'], city = city, prognosis = prognosis)
    except:
            search_error = 'error'
            return render_template('main.html', search_error = search_error)


@app.route('/', methods = ['POST'])
@app.route('/<city>', methods = ['POST'])
def search(city = None):
    input_text = request.form['text']
    if input_text.isdigit():
        search_error = 'error'
        return render_template('main.html', search_error = search_error)
    else:
        return redirect(url_for('city_search', city = input_text))


if __name__ == '__main__':
    app.run(debug=True)
