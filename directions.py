import os
import re
import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key="AIzaSyDHLHlNTnqhdo6oNo8PfErtmA5-JLvozK0")

def getDirections(fromLocation, toLocation, mode, language):
    directions = ""
    directions_result = gmaps.directions(fromLocation,toLocation,mode=mode, departure_time=datetime.now(),language=language)
    for steps in directions_result[0]['legs'][0]['steps']:
        step = steps['html_instructions']
        directions += step + ". "

    removeTags = re.compile('<.*?>')
    directions = re.sub(removeTags, '', directions)
    return directions


directions = getDirections("L5B 1E1","Austin Texas","driving","en")
if len(directions) > 1600:
    d = [directions[i:i + 1600] for i in range(0, len(directions), 1600)]
    print(len(d[0]))