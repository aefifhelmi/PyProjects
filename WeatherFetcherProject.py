import requests

API_KEY = "43bc1b5f79298c50e01541a185c4471c"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

city = input("Enter your city name: ")

request_url = f"{BASE_URL}?appid={API_KEY}&q={city}" #request_url is consist of base url, api key and user input (?appid= and $q=). f string is useful to make this url usable for every values
response = requests.get(request_url) #using requests module by GET requests

if response.status_code == 200: #status_code is a built-in py func. 200 status code means the GET request is succesful, while 404 is ERROR
    data = response.json()
    weather = data['weather'][0]['description'] #ways to fetch the data in a list/dictionaries
    temperature = round(data['main']['temp'] - 273.15, 2) #the data only shows the temp unit in K, convert it to C and round the values.

    print(weather)
    print(temperature)
else:
    print("Error occured.")
    

#KUALA LUMPUR DATA FROM API (fetch all the data needed in this whole data to simplify our programme and make it more readable)

#{'coord': {'lon': 101.6865, 'lat': 3.1431}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 
#'base': 'stations', 'main': {'temp': 299.69, 'feels_like': 299.69, 'temp_min': 298.13, 'temp_max': 300.37, 'pressure': 1011, 'humidity': 73},  
#'visibility': 10000, 'wind': {'speed': 0.51, 'deg': 0}, 'clouds': {'all': 20}, 'dt': 1667957260, 
#'sys': {'type': 2, 'id': 2078475, 'country': 'MY', 'sunrise': 1667948243, 'sunset': 1667991405}, 'timezone': 28800, 'id': 1733046, 'name': 'Kuala Lumpur', 'cod': 200}


