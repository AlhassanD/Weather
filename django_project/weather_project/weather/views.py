from django.shortcuts import render
import requests 
def index(request):
    # Request API
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=1f42d4a797916977b0589d6043217a03'
   
    # show weather data since city
    city = 'Paris'
    r = requests.get(url.format(city)).json()
    #print(r)

    #take data
    city_weather = {
        'city' : city,
        'temperature' : r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon'],
    }
    context = {'city_weather': city_weather}
    print(city_weather)
    return render(request, 'index.html', context)

