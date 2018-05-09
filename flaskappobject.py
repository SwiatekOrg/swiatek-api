from flask import Flask,render_template
from classes import Stations,Sensors,Sensor,Station

app = Flask(__name__)

@app.route('/')
def Table():
    station = Stations()
    city_stations = station.get_city_data("Kraków")

    sensors = Sensors(city_stations)
    Czujniki = sensors.city_sensors

    czujniki_len = len(Czujniki)
    tab_czujniki_len = []
    for i in range(czujniki_len):
        tab_czujniki_len.append(len(Czujniki[i]))

    for i in range(czujniki_len):
        station.streets.append(Station(city_stations[i]['stationName']))
        for a in range(tab_czujniki_len[i]):
            station.streets[i].sensors.append(Sensor('http://api.gios.gov.pl/pjp-api/rest/data/getData/' + str(Czujniki[i][a]['id'])))

    StreetNames =[]
    AllData = []
    for i in range(czujniki_len):
        StreetNames.append(station.streets[i].street)
        AllData.append([])
        for a in range(tab_czujniki_len[i]):
            AllData[i].append([])
            AllData[i][a].append(station.streets[i].sensors[a].name)
            AllData[i][a].append(station.streets[i].sensors[a].value)
            AllData[i][a].append(station.streets[i].sensors[a].time)
            AllData[i][a].append(station.streets[i].sensors[a].percent)

    return render_template('html2.html',lista_czujnikow = czujniki_len,lista_czujnikow_len = tab_czujniki_len, all = AllData, street = StreetNames)

if __name__ == '__main__':
    app.run(port=5011, debug=True)