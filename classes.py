import json
import requests
from datetime import datetime

HEADERS = {'Content-Type': 'application/json; charset=utf-8'}

class Stations():
    def __init__(self):
        self.url = "http://api.gios.gov.pl/pjp-api/rest/station/findAll"
        self.streets = []
        self.station_data = []
        self.get_station_data()

    def get_station_data(self):
        response = requests.get(self.url, HEADERS)
        self.station_data = json.loads(response.content.decode('utf-8'))

    def get_city_data(self,city_name):
        city_data = []
        for i in range(len(self.station_data)):
            if str(self.station_data[i]['city']['name']) == city_name:
                city_data.append(self.station_data[i])
        return city_data

class Sensors():
    def __init__(self,station_list):
        self.city_sensors = []
        self.get_city_sensors(station_list)

    def get_city_sensors(self,station_list):
        for i in range(len(station_list)):
            stace = requests.get('http://api.gios.gov.pl/pjp-api/rest/station/sensors/' + str(station_list[i]['id']), HEADERS)
            self.city_sensors.append(json.loads(stace.content.decode('utf-8')))

class Sensor():
    def __init__(self,url):
        self.url = url
        self.name = None
        self.value = None
        self.time = None
        self.existing_hour_index = None
        self.percent = None
        self.get_sensor_data()

    def get_sensor_data(self):
            czujnik = requests.get(self.url,HEADERS)
            czujnik_json = json.loads(czujnik.content.decode('utf-8'))
            for x in range(len(czujnik_json['values'])):
                if czujnik_json['values'][x]['value'] != None:
                    self.existing_hour_index = x
                    break
            self.name = czujnik_json['key']
            self.value =  float(czujnik_json['values'][self.existing_hour_index]['value'])
            data = datetime.strptime(czujnik_json['values'][self.existing_hour_index]['date'], '%Y-%m-%d %H:%M:%S')
            self.time = str(data.hour) + ":" + str('%02d' % data.minute)

            indeksy_powietrza = {'SO2': 100, 'NO2': 100, 'CO': 6500, 'PM10': 60, 'PM2.5': 36, 'O3': 70, 'C6H6': 10}
            self.percent = (self.value / indeksy_powietrza[self.name]) * 100


class Station():
    def __init__(self,station_name):
        self.sensors = []
        self.street = station_name

