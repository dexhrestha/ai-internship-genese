import json

from utils import get_current_weather,get_forecast_weather

def lambda_handler(event, context):
    # TODO implement
    if event['currentIntent']['name'] == "Greeting":
        return start(event)
        
    elif event['currentIntent']['name'] == "SetLocation":
        return set_location(event)
        
    elif event['currentIntent']['name'] == "CurrentWeather":
        return get_weather(event)
        
    elif event['currentIntent']['name'] == "GetForecast":
        return get_forecast(event)
    
    else:
        return default(event)




def start(event):

    """
        Handles greetings and starts the flow        
    """
    return {
            "sessionAttributes":event["sessionAttributes"],
            "dialogAction":{
                "type":"ElicitSlot",
                "message":{
                    "contentType":"PlainText",
                    "content":"What city do you want to be your default location?"
                    # "content":"How can I help you?"
                },
                "intentName":"SetLocation",
                "slots":event['currentIntent']['slots'],
                "slotToElicit" : "Location"
            }
        }
        

def set_location(event):
    """
        Sets the default location of the user
    """

    user = event['userId']
    slots = event['currentIntent']['slots']
    location = slots['Location']
    
    return {
        "sessionAttributes":event["sessionAttributes"],
            "dialogAction":{
                "type":"ElicitIntent",
                "message":{
                    "contentType":"PlainText",
                    "content":f"You have set {location} as location." + " How can I help?" 
                },
            }
    }
    
def get_location():
    """
        Reads location of specific user from database. 
        TODO
    """
    f = open('location.txt','r')
    return f.read()

def get_weather(event):

    """
        Provides current weather status of a given location      
    """

    slots = event['currentIntent']['slots']
    
    location = slots['Location'] if slots['Location'] != "None" else get_location()
    
    # content = f"Sorry I cannot get you the required information location ={location} "
    content,card = get_current_weather(location)
    
    return {
        "sessionAttributes":event["sessionAttributes"],
            "dialogAction":{
                "type":"ElicitIntent",
                "message":{
                    "contentType":"PlainText",
                    "content":content
                },
                "responseCard":card
            }
    }

def get_forecast(event):
    """
        Provides  weather forecast of a given location at a given time
    """
    slots = event['currentIntent']['slots']
    time =  slots['Time']
    location = slots['Location']
    content,card = get_forecast_weather(time,location)
    return{
        "sessionAttributes":event["sessionAttributes"],
            "dialogAction":{
                "type":"ElicitIntent",
                "message":{
                    "contentType":"PlainText",
                    "content":content
                },
                "responseCard":card
            }
    }
    

def default(event):
    """
        Serves the Fallback intent   
    """
return {
        "sessionAttributes":event["sessionAttributes"],
        "dialogAction":{
            "type":"ElicitIntent",
            "message":{
                "contentType":"PlainText",
                "content":"Sorry I could not understand you. Please try a new query."
            },
        }
    }