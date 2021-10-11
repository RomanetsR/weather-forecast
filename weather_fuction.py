import requests
from datetime import datetime
from dotenv import dotenv_values

class Weather_client:

    def __init__(self, city):

        self.city = city
        config = dotenv_values(".env") 
        self.api = config['API']
        res = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={self.city}&appid={self.api}&units=metric&exclude=daily")
        self.data = res.json()

    def weather_actual(self):
        
        time_zone = int(self.data['city']['timezone'])
        temperature = int(self.data['list'][0]['main']['temp'])
        day_of_week = datetime.fromtimestamp(self.data['list'][0]['dt'] - time_zone).strftime("%A")
        weather_description = self.data['list'][0]['weather'][0]['description']
        day_info = {'day_name' : day_of_week, 'temp' : temperature, 'description' : weather_description}

        return day_info

    def weather_prognosis(self):

        week_info = []
        temperature = [[]]
        day_of_week = [[]]
        weather_description = [[]]
        time_zone = int(self.data['city']['timezone'])
        day_index = 0
        day_of_week[day_index] = datetime.fromtimestamp(self.data['list'][0]['dt']-time_zone).strftime("%A")

        for info_block in self.data['list']:
        
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
            week_info[day_index]['description'] = (weather_description[day_index][int(len(weather_description[day_index])/2)]).lower()
            
        return week_info

