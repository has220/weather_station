from requests import get
import matplotlib.pyplot as plt
from dateutil import parser
from pprint import pprint

url = 'https://apex.oracle.com/pls/apex/raspberrypi/weatherstation/getallmeasurements/505307'

weather = get(url).json()
data = weather['items']

#get 9 pages (one month) of weather data
pages = 1
while 'next' in weather and pages <= 9:
	url = weather['next']['$ref']
	print('URL: {0}'.format(url))
	weather = get(url).json()
	data += weather['items']
	pages += 1


temperatures = [record['ambient_temp'] for record in data]
timestamps = [parser.parse(record['reading_timestamp']) for record in data]

#display the weather data 
plt.plot(timestamps, temperatures)
plt.title("Weather Station Plot - One Month")
plt.xlabel("Date and Time")
plt.ylabel("Temperature")
plt.show()