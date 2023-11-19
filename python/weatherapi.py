import json 
import requests 
 
print('Please enter your zip code:') 
zip = input() 
 
r = requests.get('http://api.openweathermap.org/data/2.5/weather?zip=%s,us&appid=d4d676a41a37055a37714f4a3d0353cd' % zip) 
data=r.json() 
print(data['weather'][0]['description']) 