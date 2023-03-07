from colorama import Fore, Back, Style
import json
import paho.mqtt.client as mqtt
from .models import Bus
from django.contrib.gis.geos import Point

def on_connect(client, userdate, flags, rc):
    client.subscribe("/hfp/v2/journey/ongoing/vp/bus/+/+/+/+/+/+/+/2/#")
    client.subscribe("/hfp/v2/journey/ongoing/dep/bus/+/+/+/+/+/+/+/+/#")
    client.subscribe("/hfp/v2/journey/ongoing/vjout/bus/+/+/+/+/+/+/+/+/#")
    

def on_message(client, userdata, message):
    result = json.loads(message.payload.decode("utf-8"));
    print(Fore.GREEN if "VP" in result else Fore.RED, "\nreceived message: " ,str(result))
    if ("VP" in result):
        result = result["VP"]
        busnumber, created = Bus.objects.update_or_create(
            busID=result["veh"], 
            defaults={
                    "route":result["desi"], 
                    "operator": result["oper"], 
                    "location": Point(result["long"], result["lat"], srid=4326),
                    "updated": result["tst"]
            }
        )
        if(not created):
            print("Updated existing record.")
    elif ("DEP" in result):
        result = result["DEP"]
        busnumber, created = Bus.objects.update_or_create(
            busID=result["veh"], 
            defaults={
                    "route":result["desi"], 
                    "operator": result["oper"], 
                    "location": Point(result["long"], result["lat"], srid=4326),
                    "updated": result["tst"],
                    "lastStop": result["stop"]

            }
        )
    elif ("VJOUT" in result):
        bus = Bus.objects.filter(busID=result["VJOUT"]["veh"])
        bus.delete()
    

mqttBroker ="mqtt.hsl.fi"

client = mqtt.Client()
client.connect(mqttBroker) 

client.on_connect=on_connect
client.on_message=on_message