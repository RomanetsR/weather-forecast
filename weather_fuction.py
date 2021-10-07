import requests
from datetime import datetime


def weather_actual(city, api_key):
    res = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&exclude=daily")
    data = res.json()
    time_zone = int(data['city']['timezone'])
    temperature = int(data['list'][0]['main']['temp'])
    day_of_week = datetime.fromtimestamp(data['list'][0]['dt'] - time_zone).strftime("%A")
    weather_description = data['list'][0]['weather'][0]['description']

    weather_now = {'day_name' : day_of_week, 'temp' : temperature, 'description' : weather_description}
    
    return weather_now

def weather_prognosis(city, api_key):
    res = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&exclude=daily")
    data = res.json()
    week_info = []
    temperature = [[]]
    day_of_week = [[]]
    weather_description = [[]]
    time_zone = data['city']['timezone']
    day_index = 0
    day_of_week[day_index] = datetime.fromtimestamp(data['list'][0]['dt']-time_zone).strftime("%A")

    for info_block in data['list']:
    
        if datetime.fromtimestamp(info_block['dt']-time_zone).strftime("%A") != day_of_week[day_index]:
            day_of_week.append([])
            temperature.append([])
            weather_description.append([])
            day_index +=1
            day_of_week[day_index] = datetime.fromtimestamp(info_block['dt']-time_zone).strftime("%A")

        temperature[day_index].append(int(info_block['main']['temp']))
        weather_description[day_index].append(info_block['weather'][0]['main'])

    for day_index in range (0, len(day_of_week)):
        week_info.append({})
        week_info[day_index]['day_name'] = day_of_week[day_index]
        week_info[day_index]['temp_max'] = max(temperature[day_index])
        week_info[day_index]['temp_min'] = min(temperature[day_index])
        week_info[day_index]['description'] = weather_description[day_index][int(len(weather_description[day_index])/2)]
        
    return week_info

