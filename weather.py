#fetching data from weather stations

from requests import get
import json
from pprint import pprint
from haversine import haversine
from dateutil import parser
import matplotlib.pyplot as plt

stations = 'https://apex.oracle.com/pls/apex/raspberrypi/weatherstation/getallstations'
weather = 'https://apex.oracle.com/pls/apex/raspberrypi/weatherstation/getallmeasurements/'

#find closest weather station from these coordinates
#Fredericksburg, VA 
my_lat = 38.303184
my_lon = -77.460540

all_stations = get(stations).json()['items']

#find the closest station from above coordinates
def find_closest():
	smallest = 20036

	for station in all_stations:
		station_lon = station['weather_stn_long']
		station_lat = station['weather_stn_lat']
		distance = haversine(my_lon, my_lat, station_lon, station_lat)
		if distance < smallest:
			smallest = distance
			closest_station = station['weather_stn_id']
	return(closest_station)



#add the weather station id number to the 'weather' URL
closest_stn = find_closest()
weather = weather + str(closest_stn)
my_weather = get(weather).json()

temperatures = [record['ambient_temp'] for record in my_weather['items']]
timestamps = [parser.parse(record['reading_timestamp']) for record in my_weather['items']]

#graph the data
plt.plot(timestamps, temperatures)
plt.xlabel('Time')
plt.ylabel('Temperature')
plt.title('Raspberry Pi Weather Station Plot')
plt.show()