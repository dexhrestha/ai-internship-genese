# from botocore.vendored i/mport requests
import urllib3
http = urllib3.PoolManager()
import json



API_KEY = "135a5fb9801a4571bce160650200610"




def get_current_weather(location):
    URL = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}"
    key = f"&q={location}"
    # res = requests.get(URL+key)
    res = http.request('GET',
                    URL+key,
                   )
    if res.status == 200:
        res = json.loads(res.data)
        weather = res['current']
        # print(weather)
        content = f"Currently the weather of {res['location']['name']},{res['location']['country']} is {weather['condition']['text']}. The current temperature is {weather['temp_c']}°C/{weather['temp_f']}°F."
        card_content = [
            {
             "title":"Current Weather",
             "subTitle":weather['condition']['text'],
             "imageUrl":"http:"+weather['condition']['icon'],
             "attachmentLinkUrl":"https://cdn1.vectorstock.com/i/1000x1000/71/80/weather-icon-with-sun-and-clouds-vector-11107180.jpg",
             "buttons":[ 
                 {
                    "text":"Hourly",
                    "value":f"Hourly weather of {location}"
                 }
              ]
           } 
            ]
        card = {
          "version": '0',
          "contentType": "application/vnd.amazonaws.card.generic",
          "genericAttachments": card_content
            }        
        return content,card
    else:
        content = "Sorry I cannot understand the location"
        return content,None

def get_forecast_weather(time,location):
    URL = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}"
    time_dict = {'today':1,'tomorrow':2}
    
    key = f"&q={location}"
    
    d_key = f"&days={time_dict[time]}" if time is not None else  f"&days=1"
    res = http.request('GET',
                    URL+key+d_key,
                  )
    if res.status == 200:
        res = json.loads(res.data)
        
        if time == 'today' or time is None:
            forecast = res['forecast']['forecastday'][0]
        if time == 'tomorrow':
            forecast = res['forecast']['forecastday'][1]
        
        content = f"The weather of {res['location']['name']},{res['location']['country']} will be {forecast['day']['condition']['text']} . The average temperature will be {forecast['day']['avgtemp_c']}°C/{forecast['day']['avgtemp_f']}°F"
        # the weather of {location} is {forecast['condition']['text']}. The current temperature is {forecast['temp_c']}°C/{forecast['temp_f']}°F".
        # f"The weather of {location} will be {forecast["day"]["condition"]["text"]}. The average temperature will be {forecast["day"]["avgtemp_c"]}/{forecast["day"]["avgtemp_f"]}"
        card_content = [ generate_card(x['time'].split()[-1],x['condition']['text'],x['condition']['icon']) for x in forecast['hour'] ]
        card_content = card_content[:10]
        card = {
          "version": '0',
          "contentType": "application/vnd.amazonaws.card.generic",
          "genericAttachments": card_content
            }        
        return content,card
    else:
        content = "Sorry I cannot understand the location"
        return content,None
        

def generate_card(title,subTitle,icon):
    return {
             "title":title,
             "subTitle":subTitle,
             "imageUrl":"http:"+icon,
             "attachmentLinkUrl":"http://www.weatherapi.com/",
             "buttons":[ 
                 {
                    "text":"Details",
                    "value":"http://www.weatherapi.com/"
                 }
              ]
           }