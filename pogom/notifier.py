import json
from pushbullet import Pushbullet
from datetime import datetime, timedelta
from .utils import get_pokemon_name, get_args
import sys
import configargparse
import logging

# Fixes the encoding of the male/female symbol
reload(sys)
sys.setdefaultencoding('utf8')

pushbullet_client = None
wanted_pokemon = None
unwanted_pokemon = None

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(module)11s] [%(levelname)7s] %(message)s')

logger = logging.getLogger(__name__)


args = get_args()


# Initialize object
def init():
    global pushbullet_client, wanted_pokemon, unwanted_pokemon, north_boundry, south_boundry, east_boundry, west_boundry,my_channel
    # load pushbullet key
    api_key = _str("o.gEylVBAd3KEXImwz8XQilpRJZ5wMU1hZ")
    pushbullet_client = Pushbullet(api_key)
    wanted_pokemon = args.notify.split(",")
    #wanted_pokemon = _str('charmander,charmeleon,charizard,squirtle,wartortle,blastoise,pikachu,raichu,sandslash,vulpix,ninetales,nidoqueen,nidoking,growlithe,arcanine,alakazam,rapidash,onix,voltorb,electrode,kangaskhan,jynx,magmar,aerodactyl,dratini,magnemite,electabuzz,hitmonchan,hitmonlee,chansey,lapras,snorlax,porygon,mew,mewtwo,moltres,zapdos,articuno,ditto,seel,gyarados') . split(",")
    wanted_pokemon = [a.lower() for a in wanted_pokemon]
    #set channel
    my_channel = pushbullet_client.channels['tag'==args.channel]
    #set boundries
    topleft = str(args.notify_topleft).split(",")
    bottomright = str(args.notify_bottomright).split(",")
    center = args.location.split(",")
    if 1 == 1:
        topleft = [(float(center[0])+0.01),(float(center[1])+0.01)]
        bottomright = [(float(center[0])-0.01),(float(center[1])-0.01)]
    north_boundry = topleft[0]
    logger.info( "[^] North bound Set:" + str(north_boundry))
    south_boundry = bottomright[0]
    logger.info( "[v] South bound Set:" + str(south_boundry))
    west_boundry = topleft[1]
    logger.info( "[<] West bound Set:" + str(west_boundry))
    east_boundry = bottomright[1]
    logger.info( "[>] East bound Set:" + str(east_boundry))
    

# Safely parse incoming strings to unicode
def _str(s):
  return s.encode('utf-8').strip()

  

  
  
# Notify user for discovered Pokemon
def pokemon_found(id,lat,log,dt):
    #pushbulley channel 
    # Or retrieve a channel by its channel_tag. Note that an InvalidKeyError is raised if the channel_tag does not exist

    rough_ns = ""
    rough_ew = ""
    if lat > north_boundry:
        rough_ns = "North"
    elif lat < south_boundry:
        rough_ns = "South"
     
    if log < west_boundry:
        rough_ew = "West"
    elif log > east_boundry:
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
    logger.info( "[+] Notifier found pokemon:" + str(pokename))

    #http://maps.google.com/maps/place/<place_lat>,<place_long>/@<map_center_lat>,<map_center_long>,<zoom_level>z
    latLon = '{},{}'.format(repr(lat), repr(log))
    google_maps_link = 'http://www.google.com/maps/place/{}'.format(latLon)

    notification_text = "Pokemon Found " + _str(pokename) + "!"
    #disappear_time = str(datetime.fromtimestamp(dt).strftime("%I:%M%p").lstrip('0'))+")"
    raw_dt=dt-datetime.utcnow()
    disappear_time = str(dt-datetime.utcnow())[2:-7].lstrip('0')
    time_of_disappear = str((datetime.utcnow()+raw_dt - timedelta(hours=5)).strftime("%I:%M%p").lstrip('0'))
    disappear_min = disappear_time[:2]
    disappear_sec = disappear_time[3:]
    location_text = "Location : " + rough_location + ". " + _str(pokename) + " Available until " +time_of_disappear+ "(" + disappear_time + " left)."
    #push = pushbullet_client.push_link(notification_text, google_maps_link, body=location_text, channel=my_channel)
    #push = pushbullet_client.push_link(notification_text, google_maps_link, body=location_text)
    push = my_channel.push_link(notification_text, google_maps_link, body=location_text)


init()
