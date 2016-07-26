import json
from pushbullet import Pushbullet
from datetime import datetime
from .utils import get_pokemon_name
import sys
import configargparse


# Fixes the encoding of the male/female symbol
reload(sys)
sys.setdefaultencoding('utf8')

pushbullet_client = None
wanted_pokemon = None
unwanted_pokemon = None



# Initialize object
def init():
    global pushbullet_client, wanted_pokemon, unwanted_pokemon
    # load pushbullet key
    api_key = _str("o.gEylVBAd3KEXImwz8XQilpRJZ5wMU1hZ")
    pushbullet_client = Pushbullet(api_key)
    wanted_pokemon = _str('pidgey,charmander,eevee') . split(",")
    wanted_pokemon = [a.lower() for a in wanted_pokemon]

# Safely parse incoming strings to unicode
def _str(s):
  return s.encode('utf-8').strip()

  

  
  
# Notify user for discovered Pokemon
def pokemon_found(id,lat,log,dt):
    #pushbulley channel 
    # Or retrieve a channel by its channel_tag. Note that an InvalidKeyError is raised if the channel_tag does not exist
    my_channel = pushbullet_client.channels[0]
    rough_location = ""
    rough_ns = ""
    rough_ew = ""
    if lat > 37.62:
        rough_ns = "North"
    elif lat < 37.6:
        rough_ns = "South"
     
    if log < -93.42:
        rough_ew = "West"
    elif log > -93.40:
        rough_ew = "East"

    if rough_ns == "" and rough_ew == "":
        rough_location = "Downtown"
    elif rough_ns == "":
        rough_location = rough_ew
    elif rough_ew == "":
        rough_location = rough_ns
    else:
        rough_location = rough_ns + "-" + rough_ew
    
    # get name
    pokename = get_pokemon_name(id)
    pokename_search = pokename.lower()
    # check array
    if not pushbullet_client:
        return
    elif wanted_pokemon != None and not pokename_search in wanted_pokemon:
        return
    elif wanted_pokemon == None and unwanted_pokemon != None and pokename in unwanted_pokemon:
        return
    # notify
    print "[+] Notifier found pokemon:", pokename

    #http://maps.google.com/maps/place/<place_lat>,<place_long>/@<map_center_lat>,<map_center_long>,<zoom_level>z
    latLon = '{},{}'.format(repr(lat), repr(log))
    google_maps_link = 'http://www.google.com/maps/place/{}'.format(latLon)

    notification_text = "Pokemon Found " + _str(pokename) + "!"
    #disappear_time = str(datetime.fromtimestamp(dt).strftime("%I:%M%p").lstrip('0'))+")"
    raw_dt=dt-datetime.utcnow()
    disappear_time = str(dt-datetime.utcnow())[3:-7]
    time_of_disappear = str((datetime.utcnow()+raw_dt - timedelta(hours=5)).strftime("%I:%M%p").lstrip('0'))
    disappear_min = disappear_time[:2]
    disappear_sec = disappear_time[3:]
    location_text = "Location : " + rough_location + ". " + _str(pokename) + " Available until " +time_of_disappear+ "(" + disappear_time + " left)."
    #push = pushbullet_client.push_link(notification_text, google_maps_link, body=location_text, channel=my_channel)
    #push = pushbullet_client.push_link(notification_text, google_maps_link, body=location_text)
    push = my_channel.push_link(notification_text, google_maps_link, body=location_text)


init()
