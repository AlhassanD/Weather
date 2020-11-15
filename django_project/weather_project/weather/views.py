from django.shortcuts import render, redirect
import requests 
from .models import City
from .forms import CityForm


def index(request):
    # Request API
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=1f42d4a797916977b0589d6043217a03'
    
    err_msg = ''
    message = ''
    message_class = ''
    
    #if my form in html is a method POST.
    if request.method == 'POST':
        form = CityForm(request.POST)
        
        if form.is_valid():
            # cleaned_data go take information with CityForm and since the input in html .
            new_city = form.cleaned_data['name']
            # Query count new city in database.
            existing_city_count = City.objects.filter(name=new_city).count()
            # Actually existing_city_count is 0.
            if existing_city_count == 0:
                # r go 'get request' url for new_city via input and take all data in the city
                r = requests.get(url.format(new_city)).json()
                print(r)
                if r['cod'] == 200:
                    form.save()
                    
                else:
                    err_msg = "City doesnt exist"
                    message_class = 'alert-danger'
            else:
                err_msg = "City already exist in the database!"
                
        if err_msg :
            message = err_msg
            message_class = 'alert-danger'
        
        else:
            message = 'City added successfully!'
            message_class = "alert-success"


    form = CityForm()
    cities = City.objects.all()
    weather_data = []
    
    for city in cities: 
        # Request get url and display data in Json 
        r = requests.get(url.format(city)).json()
        #To choose and add data with r 
        city_weather = {
            'city' : city,
            'temperature' : r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
        #print(city_weather)
       

        weather_data.append(city_weather)

        
    context = {
        'weather_data' : weather_data, 
        'form' : form,
        'message' : message,
        'message_class' : message_class
    }

    return render(request, 'index.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')