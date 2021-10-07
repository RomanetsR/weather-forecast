from flask import Flask
from flask import request
from urllib.request import urlopen
from flask import render_template
from weather_fuction import weather_actual
from weather_fuction import weather_prognosis
from  dotenv  import  dotenv_values
import json


config  =  dotenv_values ( ".env" ) 
api_key = config['api']

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'GET':
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            ip = request.environ['REMOTE_ADDR']
        else:
            ip = request.environ['HTTP_X_FORWARDED_FOR']
        url = f'http://ipinfo.io/{ip}/json'
        response = urlopen(url)
        data = json.load(response)
        city = data['city']
        weather = weather_actual(city,api_key)
        prognosis = weather_prognosis(city, api_key)
        
        return render_template('main.html', temperature=weather['temp'], city=city, prognosis = prognosis)

    elif request.method=='POST':
        input_text=request.form['text']
        if request.form['submit'] == 'Search':
            if input_text.isdigit():
                searchError = 'error'
                return render_template('main.html', searchError=searchError)
            else:
                try:
                    return city_search(input_text)
                except:
                    searchError = 'error'
                    return render_template('main.html', searchError=searchError)

def city_search(city):
    
        city=city.capitalize()
        weather = weather_actual(city,api_key)
        prognosis = weather_prognosis(city, api_key)
        return render_template('main.html', temperature=weather['temp'], city=city, prognosis = prognosis)


if __name__ == '__main__':
    app.run(debug=True)
