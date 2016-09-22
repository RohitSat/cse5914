import pyowm
import os


def process_input(string):
    cityid = 4509177
    owm = pyowm.OWM(os.environ['OWMAPIKEY'])
    obs = owm.weather_at_id(cityid)
    try:
        weather = obs.get_weather()
    except AttributeError:
        return "Unable to retrieve weather for the specified city"

    if("temperature" in string.lower()):
        return get_temperature(weather)
    elif("hot" in string.lower()):
        return get_temperature(weather)
    elif("cold" in string.lower()):
        return get_temperature(weather)

    elif "cloud" in string.lower():
        clouds = weather.get_clouds()
        if(clouds < 5):
            return "The sky is clear."
        elif(clouds < 50):
            return "There are scattered clouds."
        elif(clouds < 100):
            return "The sky is overcast."

    elif "wind" in string.lower():
        wind = weather.get_wind()
        windspeed = wind['speed']
        winddir = wind['deg']
        return "The wind speed is " + str(windspeed) + " miles per hour."

    elif 'humid' in string.lower():
        humidity = weather.get_humidity()
        return "The humidity is " + str(humidity) + " percent."
    else:
        status = weather.get_detailed_status()
        return "The current weather is " + status + "."


def get_temperature(weather):
    tempdict = weather.get_temperature(unit="fahrenheit")
    curtemp = tempdict['temp']
    resultstring = "The current temperature is "
    resultstring = resultstring + str(curtemp) + " degrees fahrenheit."
    return resultstring
